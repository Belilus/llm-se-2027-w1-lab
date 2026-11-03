# ADR-0005: Escalate high-severity, low-confidence issues to a human

- **Status:** Accepted (threshold provisional)
- **Date:** 2026-10-27
- **Deciders:** Course staff
- **Related:** OpenSpec `issue-routing` (Escalation); design.md open question 1

## Context

The model reports a `confidence` with each triage. When the model is unsure, there are three
options: drop the output, route it anyway, or route it and ask a human to check.

The costs are asymmetric. Under-reacting to a real high-severity issue (missed outage) costs
far more than a human spending a minute confirming a false alarm. For low and medium severity
the cost of a wrong route is just a delayed handoff between queues.

## Decision

- Escalate if `severity == critical` (regardless of confidence).
- Escalate if `severity == high` and `confidence < 0.6`.
- Otherwise do not escalate. Low-confidence low/medium issues are routed normally.
- The issue is still routed to its queue; escalation is an additional flag, not a reroute.

The threshold 0.6 is **provisional**. Self-reported LLM confidence is not calibrated. Before the
threshold is treated as final, it will be set from a reliability analysis on the dev split
(choose the value that keeps the escalation rate within maintainer capacity while catching most
mis-classified high-severity issues).

## Consequences

**Positive**
- Model uncertainty is converted into a human action where it matters most.
- Escalation volume is bounded: it applies only to the top two severity levels.

**Negative**
- Relies on a confidence signal of unknown calibration.
- If the model systematically over-reports confidence, risky issues will not be escalated.
  Monitoring escalation rate per model version is required.
- Interaction with the clarification queue (critical bug without reproduction steps) is not yet
  settled; see `design.md`.

## Alternatives considered

- **Discard low-confidence outputs** (send to `triage-manual`). Rejected: loses the useful
  part of the classification and floods the manual queue.
- **Calibrate confidence via self-consistency (sample N times, measure agreement).** Promising
  but multiplies cost by N; candidate for a future ADR that supersedes the confidence source.
