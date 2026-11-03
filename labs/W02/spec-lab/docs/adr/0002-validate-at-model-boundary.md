# ADR-0002: Validate model output with a strict schema; never coerce

- **Status:** Accepted
- **Date:** 2026-10-27
- **Deciders:** Course staff
- **Related:** OpenSpec `issue-enrichment` (Validation at the Model Boundary; Bounded Retry);
  ADR-0001

## Context

The model returns strings. Downstream code (routing, evaluation) wants typed values. Between the
two sits a choice: repair what the model said ("feature-request" → `enhancement`, 1.3 → 1.0,
"High" → `high`), or reject what doesn't fit.

Repair is attractive because it raises the success rate. But each repair rule is an unstated
guess about what the model *meant*, and these guesses accumulate silently. They are exactly the
kind of hidden behaviour a spec is meant to eliminate.

## Decision

- `TriageRecord` is a Pydantic v2 model with `frozen=True`, `extra="forbid"`, `Literal` enums,
  and `confidence: float = Field(ge=0.0, le=1.0)`.
- The **only** normalisation performed is `component: "unknown" → None`, because the signature
  instructs the model to use that token.
- Anything else that fails validation is rejected. Enrichment retries once; on a second failure
  a `TriageFailure` is emitted and routed to `triage-manual`.
- `repo` and `issue_number` are taken from the input, never from model output.

## Consequences

**Positive**
- Downstream code can trust every field; pyright strict holds beyond the boundary.
- Failure rate is visible and measurable rather than masked.
- Every value in a record was either produced by the model in-domain or copied from input.

**Negative**
- Slightly lower throughput; some issues need a human that a lenient parser would have handled.
- One retry adds latency and cost for failing issues.

## Alternatives considered

- **Lenient parsing with fuzzy mapping.** Rejected: hidden policy, untestable edge cases.
- **Constrained decoding / structured-output API.** Compatible with this ADR and may be adopted
  later; it reduces failures but does not remove the need for validation (e.g. range checks).
