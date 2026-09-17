"""Create deterministic plugin and standalone skill archives plus SHA256SUMS."""
import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import PLUGIN_FILES, validate
from portable import PORTABLE_FILES


def archive(path, entries):
    with zipfile.ZipFile(path, "w") as output:
        for name, data in entries:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            output.writestr(info, data, compresslevel=9)


def release(root, output, tag=None):
    root, output = Path(root), Path(output)
    version = validate(root)
    expected = f"v{version}"
    if tag is not None and tag != expected:
        raise ValueError(f"Tag {tag} does not match manifest {expected}")
    plugin = root / "plugins/mati-brain"
    output.mkdir(parents=True, exist_ok=True)
    full = output / f"mati-brain-{expected}.zip"
    skill = output / f"mati-brain-skill-{expected}.zip"
    hermes = output / f"mati-brain-hermes-{expected}.zip"
    archive(full, [("mati-brain/" + rel, (plugin / rel).read_bytes()) for rel in sorted(PLUGIN_FILES)])
    archive(skill, [("mati-brain/SKILL.md", (plugin / "skills/mati-brain/SKILL.md").read_bytes())])
    archive(hermes, [("mati-brain/" + rel, (root / rel).read_bytes()) for rel in sorted(PORTABLE_FILES)])
    checksums = output / "SHA256SUMS"
    checksums.write_text("".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in (full, skill, hermes)), encoding="ascii")
    return full, skill, hermes, checksums


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=Path("dist"))
    parser.add_argument("--tag")
    args = parser.parse_args()
    try:
        for path in release(args.root, args.output, args.tag): print(path)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Release failed: {exc}\n")


if __name__ == "__main__": main()
