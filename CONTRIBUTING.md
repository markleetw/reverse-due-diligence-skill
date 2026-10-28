# Contributing

Thanks for helping improve RDD. Please prioritize **research correctness, safety and user value** over adding ceremony or changing prose for its own sake.

## Before opening a PR

- Check the latest `main`, existing PRs and [research regression protocol](evals/README.md); avoid duplicating earlier work.
- For edits to `SKILL.md` or `references/`, identify a concrete failure mode, explain why the current rule is insufficient, and propose the smallest measurable change. Preserve existing capabilities unless evidence justifies a behavior change.
- For legal, financial, market or product facts, cite a primary source with the relevant date/jurisdiction. Do not turn illustrative examples into real-world claims.
- Use fictionalized fixtures; never commit private candidate offers, interview notes, recruiter messages, API tokens or proprietary company documents.
- For Python/HTML changes, keep canonical renderer parity and update relevant tests. Do not modify both the same rule in multiple competing documents.

## Local checks

```bash
python scripts/check_repo.py
python scripts/browser_test.py
```

The browser test requires Playwright and Chromium; see [the Browser QA workflow](.github/workflows/browser-qa.yml). An unavailable browser test must be marked **not run**, not passed. The research scenarios in [evals](evals/README.md) require separate human review and are not implied by green CI.

## Pull request expectations

Keep PRs focused. Describe: problem / reproducible evidence, change and non-goals, risk to existing behavior, actual tests executed, missing verification, and whether any docs or packaging need updating. Prefer Branch → PR → CI → Merge.

Do not alter `VERSION`, create Tags or publish Releases as part of an unrelated fix. Official releases are a separate maintainer-approved action.
