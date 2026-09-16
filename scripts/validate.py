"""Validate the small, public Mati Brain plugin without external dependencies."""
import argparse
import json
import re
import subprocess
from pathlib import Path

PLUGIN_FILES = (
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    ".mcp.json",
    "skills/mati-brain/SKILL.md",
    "skills/mati-brain/agents/openai.yaml",
)
ENDPOINT = "https://mati-brain-pilot.tail760c23.ts.net/mcp"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_version_bump(root, base, current):
    if not base or base == "0" * 40:
        return
    require(re.fullmatch(r"[0-9a-f]{40}", base), "Base must be a 40-character Git SHA")

    def old_bytes(path):
        result = subprocess.run(["git", "show", f"{base}:{path}"], cwd=root, capture_output=True)
        require(result.returncode == 0, f"Cannot read baseline file: {path}")
        return result.stdout

    prefix = "plugins/mati-brain/"
    changed = any((root / prefix / rel).read_bytes() != old_bytes(prefix + rel) for rel in PLUGIN_FILES)
    if changed:
        old_manifest = json.loads(old_bytes(prefix + ".codex-plugin/plugin.json"))
        old_version = old_manifest.get("version")
        require(isinstance(old_version, str) and re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", old_version), "Baseline plugin version invalid")
        require(tuple(map(int, current.split("."))) > tuple(map(int, old_version.split("."))), "Plugin payload changed without a higher manifest version")


def validate(root):
    root = Path(root)
    plugin = root / "plugins/mati-brain"
    require(plugin.is_dir() and not plugin.is_symlink(), "Plugin directory missing or linked")
    found = set()
    for path in plugin.rglob("*"):
        require(not path.is_symlink(), f"Symlink forbidden: {path}")
        require(path.is_dir() or path.is_file(), f"Special file forbidden: {path}")
        if path.is_file(): found.add(path.relative_to(plugin).as_posix())
    require(found == set(PLUGIN_FILES), f"Plugin files differ from exact allowlist: {sorted(found ^ set(PLUGIN_FILES))}")
    for rel in PLUGIN_FILES:
        path = plugin / rel
        require(path.is_file() and not path.is_symlink() and path.stat().st_size > 0, f"Required file invalid: {rel}")

    codex = read_json(plugin / ".codex-plugin/plugin.json")
    claude = read_json(plugin / ".claude-plugin/plugin.json")
    version = codex.get("version")
    require(codex.get("name") == claude.get("name") == "mati-brain", "Plugin names differ")
    require(isinstance(version, str) and re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", version), "Invalid semantic version")
    require(claude.get("version") == version, "Plugin versions differ")
    require(codex.get("mcpServers") == "./.mcp.json" and codex.get("skills") == "./skills/", "Codex paths changed")
    mcp = read_json(plugin / ".mcp.json")
    require(mcp == {"mcpServers": {"mati-brain": {"type": "http", "url": ENDPOINT}}}, "MCP endpoint or fields changed")

    for market_path in (root / ".agents/plugins/marketplace.json", root / ".claude-plugin/marketplace.json"):
        require(market_path.is_file() and not market_path.is_symlink(), f"Marketplace missing: {market_path}")
        market = read_json(market_path)
        require(market.get("name") == "mati", "Marketplace name changed")
        entries = market.get("plugins")
        require(isinstance(entries, list) and len(entries) == 1 and entries[0].get("name") == "mati-brain", "Marketplace plugin changed")
        require("version" not in entries[0] and "version" not in market, "Marketplace version override forbidden")
        source = entries[0].get("source")
        require(source == "./plugins/mati-brain" or source == {"source": "local", "path": "./plugins/mati-brain"}, "Marketplace source changed")

    skill = (plugin / "skills/mati-brain/SKILL.md").read_text(encoding="utf-8")
    require(skill.startswith("---\n") and re.search(r"(?m)^name:\s*mati-brain\s*$", skill), "Skill identity changed")
    return version


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--base", help="40-character Git baseline SHA for version-bump check")
    args = parser.parse_args()
    try:
        version = validate(args.root)
        check_version_bump(args.root, args.base, version)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        parser.exit(1, f"Validation failed: {exc}\n")
    print(f"Validated mati-brain v{version}: {len(PLUGIN_FILES)} plugin files")


if __name__ == "__main__": main()
