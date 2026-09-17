"""Release contract for the public Mati Brain plugin."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATE = ROOT / "scripts" / "validate.py"
RELEASE = ROOT / "scripts" / "release.py"
PORTABLE = ROOT / "scripts" / "portable.py"
PORTABLE_FILES = ("plugin.json", "mcp.json", "skills/mati-brain/SKILL.md")
PLUGIN_FILES = (
    ".codex-plugin/plugin.json", ".claude-plugin/plugin.json", ".mcp.json",
    "skills/mati-brain/SKILL.md", "skills/mati-brain/agents/openai.yaml",
)
ENDPOINT = "https://mati-brain-pilot.tail760c23.ts.net/mcp"


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def fixture(root):
    plugin = root / "plugins" / "mati-brain"
    write_json(root / ".agents/plugins/marketplace.json", {"name": "mati", "plugins": [{"name": "mati-brain", "source": {"source": "local", "path": "./plugins/mati-brain"}}]})
    write_json(root / ".claude-plugin/marketplace.json", {"name": "mati", "plugins": [{"name": "mati-brain", "source": "./plugins/mati-brain"}]})
    write_json(plugin / ".codex-plugin/plugin.json", {"name": "mati-brain", "version": "0.1.0", "skills": "./skills/", "mcpServers": "./.mcp.json"})
    write_json(plugin / ".claude-plugin/plugin.json", {"name": "mati-brain", "version": "0.1.0"})
    write_json(plugin / ".mcp.json", {"mcpServers": {"mati-brain": {"type": "http", "url": ENDPOINT}}})
    skill = plugin / "skills/mati-brain/SKILL.md"
    skill.parent.mkdir(parents=True, exist_ok=True)
    skill.write_text("---\nname: mati-brain\ndescription: Mati Brain\n---\nUse Mati Brain.\n", encoding="utf-8")
    agent = plugin / "skills/mati-brain/agents/openai.yaml"
    agent.parent.mkdir(parents=True, exist_ok=True)
    agent.write_text("interface:\n  display_name: Mati Brain\n", encoding="utf-8")
    return plugin


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.plugin = fixture(self.root)
        result = self.run_script(PORTABLE)
        self.assertEqual(result.returncode, 0, result.stderr)

    def run_script(self, script, *args):
        return subprocess.run([sys.executable, str(script), "--root", str(self.root), *args], text=True, capture_output=True)

    def commit_baseline(self):
        for command in (("init",), ("add", "."), ("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "baseline")):
            subprocess.run(("git", *command), cwd=self.root, check=True, capture_output=True)
        return subprocess.check_output(("git", "rev-parse", "HEAD"), cwd=self.root, text=True).strip()

    def test_changed_payload_requires_higher_version(self):
        base = self.commit_baseline()
        skill = self.plugin / "skills/mati-brain/SKILL.md"
        skill.write_text(skill.read_text() + "New instruction.\n")
        self.run_script(PORTABLE)
        result = self.run_script(VALIDATE, "--base", base)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("version", result.stderr.lower())

    def test_changed_payload_with_version_bump_passes(self):
        base = self.commit_baseline()
        skill = self.plugin / "skills/mati-brain/SKILL.md"
        skill.write_text(skill.read_text() + "New instruction.\n")
        for rel in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
            path = self.plugin / rel
            data = json.loads(path.read_text()); data["version"] = "0.1.1"; write_json(path, data)
        self.run_script(PORTABLE)
        self.assertEqual(self.run_script(VALIDATE, "--base", base).returncode, 0)

    def test_docs_only_change_needs_no_bump(self):
        base = self.commit_baseline()
        docs = self.root / "docs/maintenance.md"
        docs.parent.mkdir(); docs.write_text("New maintenance note.\n")
        self.assertEqual(self.run_script(VALIDATE, "--base", base).returncode, 0)

    def test_validates_clean_plugin(self):
        self.assertEqual(self.run_script(VALIDATE).returncode, 0)

    def test_rejects_version_mismatch_and_marketplace_override(self):
        path = self.plugin / ".claude-plugin/plugin.json"
        write_json(path, {"name": "mati-brain", "version": "0.2.0"})
        self.assertNotEqual(self.run_script(VALIDATE).returncode, 0)
        write_json(path, {"name": "mati-brain", "version": "0.1.0"})
        market = self.root / ".claude-plugin/marketplace.json"
        data = json.loads(market.read_text()); data["plugins"][0]["version"] = "0.1.0"; write_json(market, data)
        self.assertNotEqual(self.run_script(VALIDATE).returncode, 0)

    def test_rejects_endpoint_tampering_and_secret_fields(self):
        path = self.plugin / ".mcp.json"
        write_json(path, {"mcpServers": {"mati-brain": {"type": "http", "url": "https://example.com/mcp"}}})
        self.assertNotEqual(self.run_script(VALIDATE).returncode, 0)
        write_json(path, {"mcpServers": {"mati-brain": {"type": "http", "url": ENDPOINT, "headers": {"Authorization": "Bearer secret"}}}})
        self.assertNotEqual(self.run_script(VALIDATE).returncode, 0)

    def test_rejects_extra_plugin_file_and_symlink(self):
        (self.plugin / "secret.env").write_text("secret")
        self.assertNotEqual(self.run_script(VALIDATE).returncode, 0)
        (self.plugin / "secret.env").unlink()
        target = self.root / "outside.txt"; target.write_text("outside")
        (self.plugin / "leak").symlink_to(target)
        self.assertNotEqual(self.run_script(VALIDATE).returncode, 0)

    def test_portable_manifest_and_remote_transport(self):
        manifest = json.loads((self.root / "plugin.json").read_text())
        self.assertEqual(manifest["$schema"], "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
        self.assertEqual(manifest["name"], "mati-brain")
        self.assertEqual(manifest["version"], "0.1.0")
        self.assertNotIn("skills", manifest)
        self.assertEqual(json.loads((self.root / "mcp.json").read_text()), {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
            "mcpServers": {"mati-brain": {"type": "streamable-http", "url": ENDPOINT}},
        })
        self.assertEqual((self.root / "skills/mati-brain/SKILL.md").read_bytes(),
                         (self.plugin / "skills/mati-brain/SKILL.md").read_bytes())

    def test_rejects_stale_portable_payload(self):
        skill = self.plugin / "skills/mati-brain/SKILL.md"
        skill.write_text(skill.read_text() + "New instruction.\n")
        self.assertNotEqual(self.run_script(VALIDATE).returncode, 0)
        self.assertNotEqual(self.run_script(PORTABLE, "--check").returncode, 0)
        self.assertEqual(self.run_script(PORTABLE).returncode, 0)
        self.assertEqual(self.run_script(VALIDATE).returncode, 0)

    def test_rejects_portable_tampering_and_extra_skill(self):
        for rel in ("plugin.json", "mcp.json"):
            path = self.root / rel
            original = path.read_bytes()
            data = json.loads(original)
            data["headers"] = {"Authorization": "Bearer secret"}
            write_json(path, data)
            self.assertNotEqual(self.run_script(VALIDATE).returncode, 0)
            path.write_bytes(original)
        extra = self.root / "skills/other/SKILL.md"
        extra.parent.mkdir()
        extra.write_text("Unexpected skill")
        self.assertNotEqual(self.run_script(VALIDATE).returncode, 0)

    def test_rejects_linked_portable_paths_without_writing_target(self):
        outside = self.root / "outside"
        outside.mkdir()
        for rel in ("plugin.json", "mcp.json", "skills/mati-brain/SKILL.md"):
            path = self.root / rel
            original = path.read_bytes()
            target = outside / path.name
            target.write_bytes(original)
            path.unlink()
            path.symlink_to(target)
            self.assertNotEqual(self.run_script(VALIDATE).returncode, 0)
            self.assertNotEqual(self.run_script(PORTABLE).returncode, 0)
            self.assertEqual(target.read_bytes(), original)
            path.unlink()
            path.write_bytes(original)

    def test_first_portable_release_checks_baseline_without_portable_files(self):
        for rel in PORTABLE_FILES:
            (self.root / rel).unlink()
        base = self.commit_baseline()
        for rel in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
            path = self.plugin / rel
            data = json.loads(path.read_text())
            data["version"] = "0.2.0"
            write_json(path, data)
        self.assertEqual(self.run_script(PORTABLE).returncode, 0)
        result = self.run_script(VALIDATE, "--base", base)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_release_is_reproducible_and_tag_pinned(self):
        one = self.root / "out1"; two = self.root / "out2"
        a = self.run_script(RELEASE, "--tag", "v0.1.0", "--output", str(one))
        self.assertEqual(a.returncode, 0, a.stderr)
        b = self.run_script(RELEASE, "--tag", "v0.1.0", "--output", str(two))
        self.assertEqual(b.returncode, 0, b.stderr)
        for name in ("mati-brain-v0.1.0.zip", "mati-brain-skill-v0.1.0.zip", "mati-brain-hermes-v0.1.0.zip", "SHA256SUMS"):
            self.assertEqual((one/name).read_bytes(), (two/name).read_bytes())
        with zipfile.ZipFile(one / "mati-brain-v0.1.0.zip") as z:
            self.assertEqual(set(z.namelist()), {"mati-brain/"+p for p in PLUGIN_FILES})
        with zipfile.ZipFile(one / "mati-brain-skill-v0.1.0.zip") as z:
            self.assertEqual(z.namelist(), ["mati-brain/SKILL.md"])
        with zipfile.ZipFile(one / "mati-brain-hermes-v0.1.0.zip") as z:
            self.assertEqual(set(z.namelist()), {"mati-brain/"+p for p in PORTABLE_FILES})
            for rel in PORTABLE_FILES:
                self.assertEqual(z.read("mati-brain/"+rel), (self.root/rel).read_bytes())
        lines = (one / "SHA256SUMS").read_text().splitlines()
        self.assertEqual(len(lines), 3)
        for line in lines:
            sha, name = line.split("  ")
            self.assertEqual(sha, hashlib.sha256((one/name).read_bytes()).hexdigest())
        self.assertNotEqual(self.run_script(RELEASE, "--tag", "v0.2.0", "--output", str(self.root/"wrong")).returncode, 0)


if __name__ == "__main__": unittest.main()
