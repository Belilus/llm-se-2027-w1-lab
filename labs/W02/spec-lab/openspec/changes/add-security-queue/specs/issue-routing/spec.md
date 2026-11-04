# Spec delta: issue-routing

## ADDED Requirements

### Requirement: Security Queue
An issue is security-flagged if its `TriageRecord` has `security_suspected = true`, or if its
`TriageRecord` or `TriageFailure` has `has_security_label = true`. A security-flagged issue SHALL
be routed to queue `security`, overriding the type-based queue, `triage-clarify` and
`triage-manual`.

#### Scenario: Detected by the model
- **GIVEN** a `documentation` record with `security_suspected = true`, `has_security_label = false`
- **WHEN** routing runs
- **THEN** `queue = security`

#### Scenario: Label wins over the model
- **GIVEN** a `question` record with `security_suspected = false`, `has_security_label = true`
- **WHEN** routing runs
- **THEN** `queue = security`

#### Scenario: Security overrides the clarification queue
- **GIVEN** a security-flagged `bug` with `has_reproduction_steps = false`
- **WHEN** routing runs
- **THEN** `queue = security`

## MODIFIED Requirements

### Requirement: SLA by Severity
`sla_hours` SHALL be determined by `severity` regardless of queue:

| `severity` | `sla_hours` |
|---|---|
| `critical` | 4 |
| `high` | 24 |
| `medium` | 72 |
| `low` | 168 |

For a security-flagged issue, `sla_hours` SHALL be the lesser of 24 and the value that would
otherwise apply.

#### Scenario: SLA is unaffected by the clarify override
- **GIVEN** a `bug` with `severity = high` and `has_reproduction_steps = false`
- **WHEN** routing runs
- **THEN** `queue = triage-clarify` and `sla_hours = 24`

#### Scenario: Security issue with low severity
- **GIVEN** a security-flagged record with `severity = low`
- **WHEN** routing runs
- **THEN** `sla_hours = 24`

#### Scenario: Critical security issue keeps the shorter SLA
- **GIVEN** a security-flagged record with `severity = critical`
- **WHEN** routing runs
- **THEN** `sla_hours = 4`

### Requirement: Clarification Queue for Unreproducible Bugs
A record with `issue_type = bug` and `has_reproduction_steps = false` that is not security-flagged
SHALL be routed to `triage-clarify`, overriding the type-based queue.

#### Scenario: Bug without reproduction steps
- **GIVEN** a `bug` with `severity = medium`, `has_reproduction_steps = false`
- **WHEN** routing runs
- **THEN** `queue = triage-clarify`, `escalate = false`
- **AND** `reason` mentions missing reproduction steps

### Requirement: Escalation
`escalate` SHALL be `true` if and only if at least one of the following holds:
1. `severity = critical`;
2. `severity = high` and `confidence < 0.6`;
3. the issue is security-flagged.

Escalation SHALL apply regardless of the queue, including `triage-clarify`.

#### Scenario: Critical issue
- **GIVEN** a `question` with `severity = critical`, `confidence = 0.95`
- **WHEN** routing runs
- **THEN** `escalate = true` and `queue = support`

#### Scenario: High severity, low confidence
- **GIVEN** a `bug` with reproduction steps, `severity = high`, `confidence = 0.59`
- **WHEN** routing runs
- **THEN** `escalate = true`

#### Scenario: Confidence threshold boundary
- **GIVEN** a `bug` with reproduction steps, `severity = high`, `confidence = 0.6`
- **WHEN** routing runs
- **THEN** `escalate = false`

#### Scenario: Security issue with low severity and high confidence
- **GIVEN** a security-flagged record with `severity = low`, `confidence = 0.95`
- **WHEN** routing runs
- **THEN** `escalate = true`

#### Scenario: Critical bug without reproduction steps
- **GIVEN** a `bug` with `severity = critical`, `has_reproduction_steps = false`
- **WHEN** routing runs
- **THEN** `queue = triage-clarify`, `sla_hours = 4`, `escalate = true`

> **Note:** this last scenario fails against the current lab `router.py`, which returns early
> with `escalate = False` for every bug lacking reproduction steps. See the open question in
> `design.md`.

### Requirement: Enrichment Failures are Routed
A `TriageFailure` (see `issue-enrichment`) with `has_security_label = false` SHALL be routed to
queue `triage-manual` with `sla_hours = 72`, `escalate = false` and `reason = "enrichment failed"`.
A `TriageFailure` with `has_security_label = true` SHALL be routed to queue `security` with
`sla_hours = 24`, `escalate = true` and `reason = "enrichment failed, security label"`.

#### Scenario: Failed enrichment
- **GIVEN** a `TriageFailure` for issue `#88` with `has_security_label = false`
- **WHEN** routing runs
- **THEN** `queue = triage-manual`

#### Scenario: Failed enrichment with a security label
- **GIVEN** a `TriageFailure` for issue `#89` with `has_security_label = true`
- **WHEN** routing runs
- **THEN** `queue = security`, `sla_hours = 24`, `escalate = true`
