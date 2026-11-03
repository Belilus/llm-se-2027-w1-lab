# Change: Add LLM-assisted issue triage (enrichment + routing)

## Why

Maintainers of busy open-source repositories spend significant time reading new issues only to
decide *what kind* of issue it is, *who* should look at it, and *how urgent* it is. Much of that
first-pass judgement is pattern recognition over free text, which an LLM can approximate; the
decisions that follow from it (queue, SLA, escalation) are policy and must be predictable.

## What Changes

- **ADDED** capability `issue-enrichment`: extract structured triage fields from an issue's
  title and body using an LLM, and validate them into an immutable `TriageRecord`.
- **ADDED** capability `issue-routing`: map a validated `TriageRecord` to a queue, an SLA and an
  escalation flag using deterministic rules only.
- **ADDED** batch CLI that runs enrichment + routing over the frozen dataset and writes one
  JSON result per issue, plus an evaluation report against gold labels.
- Issue text is treated as untrusted data throughout (see ADR-0004).

Out of scope for this change: live webhook ingestion, writing labels or comments back to
GitHub, duplicate detection, assignee selection. These are candidates for later changes.

## Impact

- Affected specs: `issue-enrichment` (new), `issue-routing` (new)
- Affected code: `src/triage/schema.py`, `src/triage/extract.py`, `src/triage/router.py`,
  `src/triage/cli.py`, `tests/`
- Dependencies: DSPy, Pydantic v2; Python 3.13; `uv`; pyright in strict mode
- Decisions recorded: ADR-0001 … ADR-0005
