# Spec delta: issue-routing

## ADDED Requirements

### Requirement: Deterministic Routing
Routing SHALL be a pure function of a validated `TriageRecord`. It SHALL NOT call a model,
read the clock, perform I/O, or depend on any state other than its input and the static
routing tables below. Equal inputs SHALL produce equal outputs.

#### Scenario: Repeatability
- **GIVEN** the same `TriageRecord` routed twice
- **WHEN** routing runs
- **THEN** both results are identical

### Requirement: Routing Result
Routing SHALL produce a `Routing` value with fields `queue` (string), `sla_hours` (positive
integer), `escalate` (boolean) and `reason` (non-empty string naming the rule applied).

### Requirement: Queue by Issue Type
Unless another requirement in this spec overrides it, the queue SHALL be determined by
`issue_type`:

| `issue_type` | `queue` |
|---|---|
| `bug` | `engineering` |
| `enhancement` | `product` |
| `documentation` | `docs` |
| `question` | `support` |
| `meta` | `maintainers` |

#### Scenario: Enhancement
- **GIVEN** a record with `issue_type = enhancement`, `severity = low`
- **WHEN** routing runs
- **THEN** `queue = product`

### Requirement: SLA by Severity
`sla_hours` SHALL be determined by `severity` alone, regardless of queue:

| `severity` | `sla_hours` |
|---|---|
| `critical` | 4 |
| `high` | 24 |
| `medium` | 72 |
| `low` | 168 |

#### Scenario: SLA is unaffected by the clarify override
- **GIVEN** a `bug` with `severity = high` and `has_reproduction_steps = false`
- **WHEN** routing runs
- **THEN** `queue = triage-clarify` and `sla_hours = 24`

### Requirement: Clarification Queue for Unreproducible Bugs
A record with `issue_type = bug` and `has_reproduction_steps = false` SHALL be routed to
`triage-clarify`, overriding the type-based queue.

#### Scenario: Bug without reproduction steps
- **GIVEN** a `bug` with `severity = medium`, `has_reproduction_steps = false`
- **WHEN** routing runs
- **THEN** `queue = triage-clarify`, `escalate = false`
- **AND** `reason` mentions missing reproduction steps

### Requirement: Escalation
`escalate` SHALL be `true` if and only if at least one of the following holds:
1. `severity = critical`;
2. `severity = high` and `confidence < 0.6`.

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

#### Scenario: Critical bug without reproduction steps
- **GIVEN** a `bug` with `severity = critical`, `has_reproduction_steps = false`
- **WHEN** routing runs
- **THEN** `queue = triage-clarify`, `sla_hours = 4`, `escalate = true`

> **Note:** this last scenario fails against the current lab `router.py`, which returns early
> with `escalate = False` for every bug lacking reproduction steps. See the open question in
> `design.md`.

### Requirement: Enrichment Failures are Routed
A `TriageFailure` (see `issue-enrichment`) SHALL be routed to queue `triage-manual` with
`sla_hours = 72`, `escalate = false` and `reason = "enrichment failed"`.

#### Scenario: Failed enrichment
- **GIVEN** a `TriageFailure` for issue `#88`
- **WHEN** routing runs
- **THEN** `queue = triage-manual`

## Non-functional requirements (informative)

- **Testability:** every row of every table and every scenario above SHALL have a unit test.
  Routing is correct or incorrect — it has no accuracy metric.
- **Exhaustiveness:** adding a value to `IssueType` or `Severity` without a corresponding table
  entry SHALL be a type error (enforced via `dict[IssueType, str]` with pyright exhaustiveness
  checks or `assert_never`).
