"""Check source and release archive with an installed Hermes portable loader (offline)."""
import argparse
import sys
import tempfile
import zipfile
from pathlib import Path

from portable import PORTABLE_FILES
from validate import ENDPOINT, validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hermes-root", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.hermes_root.resolve()))
    from hermes_cli.agent_plugins import load_agent_plugin

    version = validate(args.root)

    def check(root, data):
        package = load_agent_plugin(root, data)
        if package.diagnostics:
            raise ValueError(f"Hermes diagnostics: {package.diagnostics}")
        if (package.name, package.version) != ("mati-brain", version):
            raise ValueError("Hermes package identity mismatch")
        if [skill.name for skill in package.skills] != ["mati-brain"]:
            raise ValueError("Hermes did not load the expected skill")
        if package.mcp_servers != {"mati-brain": {"url": ENDPOINT, "strict_redirect_headers": True}}:
            raise ValueError("Hermes did not load the expected remote MCP")

    with tempfile.TemporaryDirectory(prefix="mati-hermes-check-") as tmp:
        temp = Path(tmp)
        check(args.root, temp / "source-data")
        with zipfile.ZipFile(args.archive) as archive:
            expected = {"mati-brain/" + rel for rel in PORTABLE_FILES}
            if set(archive.namelist()) != expected or len(archive.namelist()) != len(expected):
                raise ValueError("Unexpected portable archive entries")
            for rel in PORTABLE_FILES:
                data = archive.read("mati-brain/" + rel)
                if data != (args.root / rel).read_bytes():
                    raise ValueError(f"Archive differs from source: {rel}")
                target = temp / "mati-brain" / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        check(temp / "mati-brain", temp / "archive-data")
    print(f"Hermes loaded source and archive: mati-brain v{version}, 1 skill, 1 remote MCP, no diagnostics")


if __name__ == "__main__":
    main()
