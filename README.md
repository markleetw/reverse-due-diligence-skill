# Reverse Due Diligence Skill

An AI agent skill for structured reverse due diligence on companies, roles, and career opportunities.

This repository is the source of truth for the **RDD** skill: a job-candidate-oriented research workflow that turns public evidence into a company/role assessment, interview questions, and a reusable HTML report.

## What it does

RDD is designed to answer three questions:

1. **Is the company structurally healthy?** — financial quality, cash flow, business-model and regulatory risk.
2. **Does the role have real scope and resources?** — ownership, KPI design, budget/headcount flexibility, reporting lines.
3. **What should the candidate ask in interviews?** — questions derived from concrete findings, not a generic interview checklist.

The workflow is intentionally evidence-heavy:

```text
Scope
  ↓
Company identity / legal entity
  ↓
Parallel research
  ↓
Deep analysis
  ↓
Evidence & uncertainty checks
  ↓
Decision synthesis
  ↓
Interview questions
  ↓
HTML report
  ↓
Deterministic audit
```

## Repository structure

```text
.
├── SKILL.md                         # Orchestrator: when to run RDD and what happens next
├── references/
│   ├── analysis-playbook.md         # Analysis methods, evidence discipline, QA heuristics
│   ├── report-template.md           # Report information architecture
│   ├── taiwan-sources.md            # Taiwan source registry
│   └── global-sources.md            # Global source registry
├── templates/
│   └── report-shell.html            # Self-contained HTML report template / chart library
├── scripts/
│   ├── audit.py                     # Generic deterministic report audit
│   └── check_repo.py                # Repository consistency checks
└── .github/workflows/
    └── ci.yml                       # CI
```

### Responsibility boundaries

- **`SKILL.md`** decides **when** to run the skill and **what step comes next**.
- **`references/`** is the canonical source for **how to research, analyze, and validate evidence**.
- **`templates/`** contains reusable output templates.
- **`scripts/`** contains deterministic tooling. Company-specific facts must not be hard-coded here.

This separation is deliberate: analytical rules should have one source of truth, while runtime-specific mechanics and report-specific assertions stay outside the core skill instructions.

## Usage

Typical invocations:

```text
/rdd Gogolook Head of Product
/rdd 台積電 Senior Product Manager 想知道值不值得接
research this company before I interview for Head of Product
```

The skill expects three inputs when available:

- company / legal entity
- role
- decision question (apply, continue interviewing, accept an offer, negotiate compensation, etc.)

If a job description or offer is available, it should be treated as first-party evidence about the role.

## Report audit

`scripts/audit.py` is generic. It receives a generated HTML report and a JSON audit spec:

```bash
python3 scripts/audit.py report.html audit-spec.json
```

The spec can define:

- stale claims that must no longer appear
- canonical values that must appear
- regex-based resolved claims
- arithmetic assertions

The audit checks **internal consistency**, not whether the underlying external facts are true. Source verification still belongs to the research workflow.

## Development principles

1. **One rule, one canonical location.** Avoid copying detailed evidence/QA rules into `SKILL.md`.
2. **No company-specific state in reusable files.** Company facts belong in generated reports/audit specs, not scripts or templates.
3. **Prefer deterministic checks for deterministic problems.** Arithmetic, stale-value scans, path/reference validation and syntax checks should not rely on LLM rereading.
4. **Keep the distributable skill simple.** The repository may have CI and tooling; the skill itself should remain understandable from a small number of files.

## Status

The project is evolving from a working personal skill into a reusable, maintainable RDD workflow. The current focus is preserving the proven research method while reducing duplicated rules and report-specific hard-coding.


## Packaging & releases

The Git repository is the source of truth. The distributable `.skill` file is a **release artifact** and is not committed back into the repository.

A release package contains only the files required at runtime:

```text
rdd/
├── SKILL.md
├── references/
├── templates/
└── scripts/
    └── audit.py
```

Development-only files such as `README.md`, `.github/`, `examples/`, and `scripts/check_repo.py` are excluded.

To build locally:

```bash
python scripts/package.py --output dist/reverse-due-diligence.skill
```

To publish a release:

```bash
git tag v0.1.0
git push origin v0.1.0
```

Pushing a `v*` tag runs CI, creates the `.skill` package, generates a SHA-256 checksum, and creates or updates the matching GitHub Release. Publishing a Release manually from GitHub also rebuilds and uploads the package for that Release tag.

The package is built deterministically: file order, ZIP timestamps, and permissions are normalized so the same source tree produces the same `.skill` bytes.
