#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the distributable reverse-due-diligence .skill package.

The .skill format is a ZIP archive whose top-level directory is "rdd/".
Only runtime files are included. Development/CI files are intentionally excluded.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = "rdd"
FIXED_TIME = (1980, 1, 1, 0, 0, 0)

INCLUDE_FILES = [
    Path("SKILL.md"),
    Path("references/analysis-playbook.md"),
    Path("references/global-sources.md"),
    Path("references/report-template.md"),
    Path("references/taiwan-sources.md"),
    Path("templates/report-shell.html"),
    Path("scripts/audit.py"),
]

EXECUTABLES = {Path("scripts/audit.py")}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build(output: Path) -> None:
    missing = [str(rel) for rel in INCLUDE_FILES if not (ROOT / rel).is_file()]
    if missing:
        raise SystemExit("Missing required runtime files:\n- " + "\n- ".join(missing))

    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_suffix(output.suffix + ".tmp")
    if tmp.exists():
        tmp.unlink()

    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel in sorted(INCLUDE_FILES, key=lambda p: p.as_posix()):
            src = ROOT / rel
            arcname = f"{PACKAGE_ROOT}/{rel.as_posix()}"
            info = zipfile.ZipInfo(arcname, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            mode = 0o755 if rel in EXECUTABLES else 0o644
            info.external_attr = (mode & 0xFFFF) << 16
            info.flag_bits |= 0x800  # UTF-8 filenames
            zf.writestr(info, src.read_bytes())

    os.replace(tmp, output)
    print(f"Built {output}")
    print(f"SHA256 {sha256(output)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "dist" / "reverse-due-diligence.skill",
        help="Output .skill path",
    )
    args = parser.parse_args()
    build(args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
