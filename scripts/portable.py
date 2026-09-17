"""Generate the root Agent Plugins v1 package from the shared plugin source."""
import argparse
import json
from pathlib import Path

PORTABLE_FILES = ("plugin.json", "mcp.json", "skills/mati-brain/SKILL.md")


def payload(root):
    plugin = Path(root) / "plugins/mati-brain"
    source = json.loads((plugin / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    manifest = {"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"}
    for key in ("name", "version", "description", "author", "homepage", "repository"):
        if key in source:
            manifest[key] = source[key]
    connection = json.loads((plugin / ".mcp.json").read_text(encoding="utf-8"))
    mcp = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
        "mcpServers": {"mati-brain": {
            "type": "streamable-http",
            "url": connection["mcpServers"]["mati-brain"]["url"],
        }},
    }
    def encode(value):
        return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    return {
        "plugin.json": encode(manifest),
        "mcp.json": encode(mcp),
        "skills/mati-brain/SKILL.md": (plugin / "skills/mati-brain/SKILL.md").read_bytes(),
    }


def sync(root, *, check=False):
    root = Path(root).resolve()
    expected = payload(root)
    # Refuse links before writing anything, including linked parent directories.
    for rel in expected:
        path = root / rel
        for component in (path, *path.parents):
            if component == root:
                break
            if component.is_symlink():
                raise ValueError(f"Symlink forbidden: {component}")
    skills = root / "skills"
    if skills.exists():
        for path in skills.rglob("*"):
            if path.is_symlink() or (not path.is_dir() and path.relative_to(root).as_posix() not in expected):
                raise ValueError(f"Unexpected portable skill file: {path}")
    for rel, data in expected.items():
        path = root / rel
        if check:
            if not path.is_file() or path.read_bytes() != data:
                raise ValueError(f"Portable file out of sync: {rel}; run python3 scripts/portable.py")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        sync(args.root, check=args.check)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Portable package failed: {exc}\n")
    print("Portable package " + ("verified" if args.check else "generated"))


if __name__ == "__main__":
    main()
