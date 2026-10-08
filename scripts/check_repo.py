#!/usr/bin/env python3
"""Repository consistency checks for reverse-due-diligence-skill."""
from __future__ import annotations

import json
import py_compile
import re
import subprocess
import sys
import tempfile
import zipfile
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)
    print(f"✗ {message}")


def ok(message: str) -> None:
    print(f"✓ {message}")


def check_frontmatter() -> None:
    path = ROOT / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        fail("SKILL.md is missing YAML-style frontmatter")
        return
    block = match.group(1)
    for key in ("name", "description"):
        if not re.search(rf"^{key}:\s*\S+", block, re.M):
            fail(f"SKILL.md frontmatter is missing {key}")
    if not ERRORS:
        ok("SKILL.md frontmatter")


def check_references() -> None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    refs = sorted(set(re.findall(r"`((?:references|templates|scripts)/[A-Za-z0-9_./-]+)`", text)))
    missing = [ref for ref in refs if not (ROOT / ref).exists()]
    if missing:
        for ref in missing:
            fail(f"SKILL.md references missing file: {ref}")
    else:
        ok(f"SKILL.md file references ({len(refs)})")


def check_template() -> None:
    path = ROOT / "templates" / "report-shell.html"
    if not path.exists():
        fail("templates/report-shell.html is missing")
        return
    text = path.read_text(encoding="utf-8")
    for placeholder in ("{{公司名}}", "{{職缺}}", "{{日期}}"):
        if placeholder not in text:
            fail(f"report template missing placeholder: {placeholder}")
    if not any(e.startswith("report template") for e in ERRORS):
        ok("report template placeholders")


def check_python() -> None:
    for rel in ("scripts/audit.py", "scripts/check_repo.py", "scripts/package.py"):
        try:
            py_compile.compile(str(ROOT / rel), doraise=True)
            ok(f"Python compile: {rel}")
        except py_compile.PyCompileError as exc:
            fail(f"Python compile failed: {rel}: {exc.msg}")


def check_forbidden_paths() -> None:
    offenders: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix not in {".md", ".py", ".html", ".yml", ".yaml", ".json"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        forbidden_root = "/" + "home/claude/"
        if forbidden_root in text:
            offenders.append(str(path.relative_to(ROOT)))
    if offenders:
        for rel in offenders:
            fail(f"absolute Claude path found in {rel}")
    else:
        ok("no absolute Claude home paths")


def check_generic_files() -> None:
    # Examples in the analysis playbook may name real companies. Reusable runtime
    # files must not carry report-specific state.
    terms = re.compile(r"\b(?:Gogolook|JUJI|Whoscall|ScamAdviser)\b", re.I)
    for rel in ("scripts/audit.py", "scripts/package.py", "templates/report-shell.html"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        match = terms.search(text)
        if match:
            fail(f"company-specific term {match.group(0)!r} found in generic file {rel}")
        else:
            ok(f"generic file is company-neutral: {rel}")


def check_runtime_portability() -> None:
    """Keep distributed instructions free of host-specific tool/API names."""
    runtime_files = [
        ROOT / "SKILL.md",
        ROOT / "references" / "analysis-playbook.md",
        ROOT / "references" / "report-template.md",
        ROOT / "templates" / "report-shell.html",
    ]
    forbidden = (
        "AskUserQuestion",
        "SendUserFile",
        "create_artifact",
        "update_artifact",
        '/opt/pw-browsers/',
        'display: "render"',
    )
    for path in runtime_files:
        text = path.read_text(encoding="utf-8")
        for term in forbidden:
            if term in text:
                fail(
                    f"host-specific runtime instruction {term!r} found in "
                    f"{path.relative_to(ROOT)}"
                )
    if not any("host-specific runtime instruction" in e for e in ERRORS):
        ok("runtime instructions are host-neutral")


def check_old_layout_references() -> None:
    text_files = [ROOT / "SKILL.md", ROOT / "references" / "report-template.md", ROOT / "README.md"]
    for path in text_files:
        text = path.read_text(encoding="utf-8")
        if "assets/report-shell.html" in text or "assets/audit-template.py" in text:
            fail(f"legacy assets/ path referenced in {path.relative_to(ROOT)}")
    if not any("legacy assets/" in e for e in ERRORS):
        ok("no legacy assets/ references")


def check_example_spec_and_audit() -> None:
    spec_path = ROOT / "examples" / "audit-spec.example.json"
    try:
        json.loads(spec_path.read_text(encoding="utf-8"))
        ok("example audit spec JSON")
    except Exception as exc:
        fail(f"invalid example audit spec: {exc}")
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        report = Path(temp_dir) / "report.html"
        report.write_text("<html><body>reference price: 126.5</body></html>", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "audit.py"), str(report), str(spec_path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            fail("generic audit smoke test failed:\n" + proc.stdout + proc.stderr)
        else:
            ok("generic audit smoke test")




def check_public_docs() -> None:
    path = ROOT / "README.md"
    if not path.exists():
        fail("missing public documentation: README.md")
        return

    readme = path.read_text(encoding="utf-8")
    for marker in (
        "<!-- release-notes:start -->",
        "<!-- release-notes:end -->",
        "ChatGPT",
        "Claude",
        "reverse-due-diligence.zip",
    ):
        if marker not in readme:
            fail(f"README missing public install marker: {marker}")

    for noise in (".skill", "SHA256SUMS"):
        if noise in readme:
            fail(f"user-facing documentation contains implementation noise {noise!r}: README.md")

    banned = [
        "Gogo" + "look",
        "JU" + "JI",
        "Who" + "scall",
        "Scam" + "Adviser",
        "走" + "著瞧",
    ]
    public_files = [
        ROOT / "README.md",
        ROOT / "SKILL.md",
        ROOT / "references" / "analysis-playbook.md",
    ]
    for public_path in public_files:
        text = public_path.read_text(encoding="utf-8")
        for term in banned:
            if term.lower() in text.lower():
                fail(f"targeted case-company term {term!r} found in {public_path.relative_to(ROOT)}")

    if not any("README missing" in e or "targeted case-company" in e or "public documentation" in e for e in ERRORS):
        ok("public README and fictionalized examples")

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_package() -> None:
    expected = {
        "rdd/SKILL.md",
        "rdd/references/analysis-playbook.md",
        "rdd/references/global-sources.md",
        "rdd/references/report-template.md",
        "rdd/references/taiwan-sources.md",
        "rdd/templates/report-shell.html",
        "rdd/scripts/audit.py",
    }
    with tempfile.TemporaryDirectory() as temp_dir:
        out1 = Path(temp_dir) / "a.skill"
        out2 = Path(temp_dir) / "b.skill"

        for out in (out1, out2):
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "package.py"), "--output", str(out)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            if proc.returncode != 0:
                fail("package build failed:\n" + proc.stdout + proc.stderr)
                return

        with zipfile.ZipFile(out1) as archive:
            actual = set(archive.namelist())
        if actual != expected:
            fail(
                "package contents mismatch: "
                f"expected={sorted(expected)}, actual={sorted(actual)}"
            )
            return

        if file_sha256(out1) != file_sha256(out2):
            fail("package build is not deterministic")
            return

        ok("package build, contents and reproducibility")

def main() -> int:
    check_frontmatter()
    check_references()
    check_template()
    check_python()
    check_forbidden_paths()
    check_generic_files()
    check_runtime_portability()
    check_old_layout_references()
    check_example_spec_and_audit()
    check_public_docs()
    check_package()

    if ERRORS:
        print(f"\n{len(ERRORS)} check(s) failed.")
        return 1
    print("\nAll repository checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
