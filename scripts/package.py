#!/usr/bin/env python3
"""Build and verify the deterministic RDD runtime ZIP.

All distribution jobs share this manifest and verification logic. The ZIP has
one top-level rdd/ directory; source, licenses and basic installation docs
travel together. Development-only files remain outside the package.
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
    Path("LICENSE"),
    Path("README.md"),
    Path("README.zh-TW.md"),
    Path("VERSION"),
    Path("references/analysis-playbook.md"),
    Path("references/global-sources.md"),
    Path("references/report-template.md"),
    Path("references/taiwan-sources.md"),
    Path("templates/report-shell.html"),
    Path("scripts/audit.py"),
]
EXECUTABLES = {Path("scripts/audit.py")}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_package(path: Path, expected_version: str | None = None) -> None:
    """Inspect the *actual* archive: names, integrity, bytes and version."""
    expected = {f"{PACKAGE_ROOT}/{rel.as_posix()}" for rel in INCLUDE_FILES}
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or set(names) != expected:
            raise ValueError(
                f"package manifest mismatch: expected={sorted(expected)}; "
                f"actual={sorted(names)}"
            )
        corrupt = archive.testzip()
        if corrupt:
            raise ValueError(f"ZIP corruption detected at {corrupt}")
        for rel in INCLUDE_FILES:
            member = f"{PACKAGE_ROOT}/{rel.as_posix()}"
            if archive.read(member) != (ROOT / rel).read_bytes():
                raise ValueError(f"archive bytes differ from source: {member}")
            entry = archive.getinfo(member)
            if entry.date_time != FIXED_TIME:
                raise ValueError(f"non-reproducible archive timestamp: {member}")
        version = archive.read(f"{PACKAGE_ROOT}/VERSION").decode("utf-8").strip()
        if expected_version and version != expected_version:
            raise ValueError(
                f"ZIP VERSION {version!r} does not match {expected_version!r}"
            )
    print(f"Verified {path}: {len(expected)} exact files, VERSION {version}")
    print(f"SHA256 {sha256(path)}")


def build(output: Path) -> None:
    missing = [str(rel) for rel in INCLUDE_FILES if not (ROOT / rel).is_file()]
    if missing:
        raise SystemExit("Missing runtime files:\n- " + "\n- ".join(missing))
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_suffix(output.suffix + ".tmp")
    if tmp.exists():
        tmp.unlink()
    with zipfile.ZipFile(
        tmp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for rel in sorted(INCLUDE_FILES, key=lambda p: p.as_posix()):
            info = zipfile.ZipInfo(
                f"{PACKAGE_ROOT}/{rel.as_posix()}", date_time=FIXED_TIME
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            mode = 0o755 if rel in EXECUTABLES else 0o644
            info.external_attr = (mode & 0xFFFF) << 16
            info.flag_bits |= 0x800
            archive.writestr(info, (ROOT / rel).read_bytes())
    os.replace(tmp, output)
    verify_package(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path,
        default=ROOT / "dist" / "reverse-due-diligence.zip",
        help="Build a deterministic ZIP at this path",
    )
    parser.add_argument(
        "--verify", type=Path,
        help="Verify an already built ZIP (no rewriting)",
    )
    parser.add_argument(
        "--expected-version", type=str,
        help="Require this VERSION inside the verified archive",
    )
    args = parser.parse_args()
    if args.verify:
        verify_package(args.verify, expected_version=args.expected_version)
    else:
        build(args.output)
        if args.expected_version:
            verify_package(args.output, expected_version=args.expected_version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
