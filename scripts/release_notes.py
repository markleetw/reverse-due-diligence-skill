#!/usr/bin/env python3
"""Build bilingual release notes from versioned Changelog entries."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADING = re.compile(r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})$")


def extract_section(text: str, version: str) -> str:
    lines = text.splitlines()
    index = next(
        (i for i, line in enumerate(lines)
         if (match := HEADING.fullmatch(line)) and match.group(1) == version),
        None,
    )
    if index is None:
        raise ValueError(f"Missing changelog entry for version {version}")
    end = next(
        (i for i in range(index + 1, len(lines))
         if lines[i].startswith("## ")),
        len(lines),
    )
    content = "\n".join(lines[index + 1:end]).strip()
    if not content:
        raise ValueError(f"Empty changelog entry for version {version}")
    return content


def make_notes(version: str, english: str, taiwan: str) -> str:
    en = extract_section(english, version)
    tw = extract_section(taiwan, version)
    return (
        f"# Reverse Due Diligence Skill v{version}\n\n"
        f"## English\n\n{en}\n\n"
        f"## 繁體中文（台灣）\n\n{tw}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"\d+\.\d+\.\d+", args.version):
        parser.error("Version must be MAJOR.MINOR.PATCH")
    notes = make_notes(
        args.version,
        (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"),
        (ROOT / "CHANGELOG.zh-TW.md").read_text(encoding="utf-8"),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(notes, encoding="utf-8")
    print(f"Prepared bilingual release notes for v{args.version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
