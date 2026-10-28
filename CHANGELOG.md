# Changelog

Notable changes are tracked here. `main` may include work that has not been packaged or released. GitHub Releases are authoritative for published Tags. Keep this file synchronized with `CHANGELOG.zh-TW.md`. Release Notes are generated only from dated, versioned sections.

## Unreleased

No changes since v1.0.0 have been recorded.

## [1.0.0] - 2026-10-28

### Research method and safety

- Strengthened primary-source provenance, legal/regulatory inference, accounting-period and denominator checks, and separation of employer health from actual role decision rights.
- Added calibrated scoring confidence and **Not Assessed** for dimensions without sufficient evidence; promoted conditional career recommendations and targeted P0/P1/P2 interview questions.
- Corrected the Taiwan pawnshop statutory-rate benchmark (Article 11: 30% annual interest) and separated financing cash-flow costs from statutory/legal applicability.
- Reinforced prompt-injection controls: external pages, job ads and attachments are untrusted evidence, never instructions to upload candidate data.

### Report delivery and regression

- Improved deterministic report audits for values extracted from the delivered HTML, arithmetic assertions, full-document envelope checks and canonical renderer parity.
- Made untrusted chart tooltip/legend labels inert text and added Chromium XSS, theme, desktop and mobile checks.
- Published full synthetic demos in Traditional Chinese and English, with matching screenshots and automated parity checks for both languages.
- Added an eight-scenario human research evaluation rubric. Five representative Claude research runs were reviewed on 2026-10-28; findings, remaining coverage and limited reproducibility are documented in `evals/README.md`. These are not statistically representative model benchmarks.

### Packaging, release governance and documentation

- Published a deterministic nine-file Skill ZIP including the MIT license and internal VERSION.
- Added protected-branch PR/CI gates and separated read-only Release Candidate checks from explicitly authorized, version-checked Release publishing.
- Added bilingual install guidance, source/safety boundaries, contribution and security documentation.

## v0.2.0 — 2026-10-08

Published as [Reverse Due Diligence Skill v0.2.0](https://github.com/markleetw/reverse-due-diligence-skill/releases/tag/v0.2.0). For historical assets and the original release notes, use the linked Release rather than attributing later changes to this Tag.

Earlier Releases: [v0.1.2](https://github.com/markleetw/reverse-due-diligence-skill/releases/tag/v0.1.2), [v0.1.1](https://github.com/markleetw/reverse-due-diligence-skill/releases/tag/v0.1.1), [v0.1.0](https://github.com/markleetw/reverse-due-diligence-skill/releases/tag/v0.1.0).
