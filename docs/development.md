# Development

RDD is maintained through small, reviewable Pull Requests. **Do not equate a successful CI run with verified real-world AI research quality.**

## Structure

- `SKILL.md`: workflow orchestration, triggers and delivery expectations.
- `references/`: Taiwan/global sources, research evidence rules and report structure.
- `templates/report-shell.html`: canonical self-contained report renderer.
- `scripts/audit.py`: deterministic report assertions and renderer parity.
- `scripts/package.py`: one deterministic package manifest and exact ZIP verifier.
- `scripts/check_repo.py`: repository checks, negative tests and package reproducibility.
- `scripts/browser_test.py`: Chromium render and dynamic-label security checks.
- `scripts/release_notes.py`: versioned bilingual Release Notes from both Changelogs.
- `evals/README.md`: human-reviewed research regression scenarios, with dated status and known evidence limits.

## Local checks

```bash
python scripts/check_repo.py
python scripts/browser_test.py  # requires Playwright + Chromium
python scripts/package.py --output dist/reverse-due-diligence.zip
python scripts/package.py --verify dist/reverse-due-diligence.zip --expected-version "$(cat VERSION)"
python scripts/audit.py report.html audit-spec.json --renderer-template templates/report-shell.html
```

## Release process (manual approval required)

1. Complete and review the relevant research/CI/Browser QA changes via PRs. Keep important user-facing behavior intact.
2. Create a separate version-preparation PR: update `VERSION`, and move the relevant `Unreleased` entries into identical `## [X.Y.Z] - YYYY-MM-DD` sections in `CHANGELOG.md` and `CHANGELOG.zh-TW.md`. Check all links and documentation.
3. Merge that PR only after CI. **Updating VERSION or pushing to main does not create a Tag or Release.**
4. After explicit maintainer approval, dispatch **Release** once from `main` with the *new* `vX.Y.Z` tag. The workflow checks the source commit and VERSION, runs repository and Chromium tests, verifies the ZIP and checksum, and builds bilingual notes **before** creating a Tag or publishing.
5. Verify the created Tag, Release Notes, ZIP, SHA-256 checksum and successful Actions run. Existing published Release assets are never overwritten by the normal workflow.

Versioned historical Releases remain immutable. A failed release after Tag creation may be retried only against the same exact source commit while no published Release exists; any other correction needs explicit maintainer review.

## Evaluation

Follow [`evals/README.md`](../evals/README.md). Use the dated results register: mark exact unexecuted fixtures **NOT RUN**, and distinguish private human-reviewed artifacts from publicly reproducible evidence. `check_repo.py` and Browser QA validate deterministic/repository behavior only.
