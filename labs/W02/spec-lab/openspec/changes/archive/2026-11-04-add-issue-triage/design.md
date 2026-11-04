# Design: add-issue-triage

## Context

The feature combines a probabilistic component (an LLM reading free text) with a policy
component (queues, SLAs, escalation). The central design goal is to keep the boundary between
the two narrow, typed, and testable, so that uncertainty from the model cannot leak into policy
except through validated fields.

## Pipeline

```
issue JSON ──► extract.py ──► schema.py ──► router.py ──► results/*.json
 (untrusted)    (LLM via       (Pydantic     (pure
                 DSPy)          validation)   function)
                  │                 │
                  └── retry ×1 ─────┘──► TriageFailure ──► triage-manual
```

## Decisions

| # | Decision | ADR |
|---|---|---|
| D1 | Separate LLM extraction from deterministic routing | [ADR-0001](../../../docs/adr/0001-separate-extraction-from-routing.md) |
| D2 | Validate model output with a frozen Pydantic model; never coerce | [ADR-0002](../../../docs/adr/0002-validate-at-model-boundary.md) |
| D3 | Use DSPy signatures instead of hand-written prompts | [ADR-0003](../../../docs/adr/0003-dspy-for-extraction.md) |
| D4 | Treat issue text as untrusted data | [ADR-0004](../../../docs/adr/0004-issue-text-is-untrusted.md) |
| D5 | Escalate on low confidence rather than discard low-confidence output | [ADR-0005](../../../docs/adr/0005-escalate-on-low-confidence.md) |

## Type boundaries

- `extract.py` is the only module that touches untyped values (`str` fields returned by DSPy).
- `schema.py` defines `IssueType` and `Severity` as `Literal` types, and `TriageRecord` with
  `frozen=True, extra="forbid"`.
- `router.py` imports only from `schema.py`; it takes `TriageRecord | TriageFailure` and returns
  `Routing`. pyright strict runs on the whole package.

## Risks / Trade-offs

- **Confidence is self-reported** by the model and is not calibrated. The 0.6 threshold is a
  placeholder; ADR-0005 records the plan to calibrate it on the dev split.
- **Severity is subjective.** Gold labels in the frozen dataset have non-trivial
  inter-annotator disagreement; the quality target uses within-one-level agreement for that
  reason.
- **Retry doubles cost** for failing issues; bounded at one retry.

## Open Questions

1. **Critical bugs without reproduction steps.** The spec requires that they go to
   `triage-clarify` *and* escalate. The current lab `router.py` returns early and never
   escalates them. Which is right? Arguments: escalating an issue nobody can reproduce wastes
   on-call time; not escalating a potentially critical bug risks missing an outage.
   *Decision pending — the spec states the conservative choice.*
2. Should `component` be constrained to a per-repo enum (from `config/repos.toml`) rather than
   free text? Deferred to a later change.
