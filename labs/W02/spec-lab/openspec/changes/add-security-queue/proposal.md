# Change: Send security issues to a security queue

## Why

A vulnerability report against hono was filed as a normal issue. Triage sent it to `engineering`
and it sat in a public queue for three days before anyone noticed. The triage lead asked in CR-1
that security issues go to a private `security` queue, reach a human straight away and be handled
within 24 hours. The model should detect them from the text, and an existing `security` label
should count too.

## What Changes

- **ADDED** a `security_suspected` field, produced by the model from title and body.
- **ADDED** a `has_security_label` field, computed from the input labels without the model. It
  appears on both `TriageRecord` and `TriageFailure`.
- **ADDED** a security recall target for `security_suspected`.
- **ADDED** routing rule: a security-flagged issue goes to the `security` queue. This overrides the
  type-based queue, `triage-clarify` and `triage-manual`.
- **MODIFIED** SLA: a security-flagged issue gets at most 24 hours. A critical one keeps 4 hours.
- **MODIFIED** escalation: every security-flagged issue is escalated.
- **MODIFIED** enrichment input: labels are now read, but they still never reach the model.
- **BREAKING** `TriageRecord` and `TriageFailure` gain required fields.

Out of scope:

- Access control. The system only emits a queue name, so keeping the queue private is the job of
  whatever consumes the output.
- Notifying a human. `escalate = true` is all this system emits.
- Measuring real response time. The system emits `sla_hours` and cannot see what people do.

Assumptions to confirm with the triage lead:

- The security label is exactly `security`, in any case. Labels like `area/security` or
  `vulnerability` do not count.
- A label wins over the model, even if the model says the issue is not a security issue.
- A failed enrichment with no security label stays in `triage-manual`, because nothing says it is
  a security issue. A real vulnerability can still wait 72 hours on this path.
- The recall target of 0.95 is proposed by me and does not come from CR-1.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `issue-enrichment`
- `issue-routing`

## Impact

- Affected code: `src/triage/schema.py`, `src/triage/extract.py`, `src/triage/router.py`, `tests/`
- Affected docs: `docs/srs-excerpt.md` version 0.4, and `docs/user-stories.md` (US-01 says labels
  are not used)
- The model prompt changes, because the model has one more field to fill
- Gold security labels are needed to measure recall
