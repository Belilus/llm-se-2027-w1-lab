# Tasks: add-issue-triage

## 1. Schema
- [ ] 1.1 Define `IssueType` and `Severity` as `Literal` types in `schema.py`
- [ ] 1.2 Define `TriageRecord` (frozen, `extra="forbid"`, `confidence` in [0, 1])
- [ ] 1.3 Define `TriageFailure` (`repo`, `issue_number`, `reason`, `raw_output` ≤ 2,000 chars)
- [ ] 1.4 Unit tests: valid record; each invalid field rejected; `unknown` component → `None`

## 2. Routing (no model calls)
- [ ] 2.1 Implement `route(record: TriageRecord | TriageFailure) -> Routing`
- [ ] 2.2 Type the tables as `dict[IssueType, str]` and `dict[Severity, int]`
- [ ] 2.3 One test per table row (5 queues, 4 SLAs)
- [ ] 2.4 One test per scenario in `specs/issue-routing/spec.md`, including the 0.6 boundary
       and the critical-bug-without-repro case
- [ ] 2.5 Property test: `route` is deterministic over generated records

## 3. Extraction
- [ ] 3.1 DSPy `TriageSignature` with the five output fields
- [ ] 3.2 Build `TriageRecord` with `repo` / `issue_number` from input, never from output
- [ ] 3.3 Retry once on validation failure; emit `TriageFailure` otherwise
- [ ] 3.4 Tests with a stubbed LM: valid output, invalid-then-valid, invalid twice

## 4. Security
- [ ] 4.1 Grep-based CI check: no `subprocess`, `os.system`, `shell=True`, or `eval` in `src/triage/`
- [ ] 4.2 Fixture issues containing shell substitution and prompt injection; assert no
       process spawn and schema-only output

## 5. CLI and evaluation
- [ ] 5.1 `triage run --split dev` writes one JSON per issue with `LLM_MODEL` in metadata
- [ ] 5.2 `triage eval` reports macro-F1 (`issue_type`) and within-one agreement (`severity`)
- [ ] 5.3 Response cache keyed by (model, issue) for reproducible reruns

## 6. Gates
- [ ] 6.1 `pyright --strict` passes with zero errors
- [ ] 6.2 All tests pass
- [ ] 6.3 `openspec validate add-issue-triage --strict` passes
- [ ] 6.4 Resolve or explicitly defer open question 1 in `design.md`
