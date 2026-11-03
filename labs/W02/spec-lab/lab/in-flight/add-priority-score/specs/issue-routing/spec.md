# Spec delta: issue-routing

## ADDED Requirements

### Requirement: Issue Priority
Each issue SHALL be assigned a priority from `P1` (most urgent) to `P4`, determined by its
severity and by the number of 👍 reactions the issue has on GitHub:

| `severity` | fewer than 10 👍 | 10 👍 or more |
|---|---|---|
| `critical` | `P1` | `P1` |
| `high` | `P2` | `P1` |
| `medium` | `P3` | `P2` |
| `low` | `P4` | `P3` |

#### Scenario: Popular medium-severity issue
- **GIVEN** an issue with `severity = medium` and 25 👍 reactions
- **WHEN** routing runs
- **THEN** its priority is `P2`

#### Scenario: Unpopular high-severity issue
- **GIVEN** an issue with `severity = high` and 3 👍 reactions
- **WHEN** routing runs
- **THEN** its priority is `P2`

## MODIFIED Requirements

### Requirement: SLA by Severity
`sla_hours` SHALL be determined by the issue's priority:

| priority | `sla_hours` |
|---|---|
| `P1` | 4 |
| `P2` | 24 |
| `P3` | 72 |
| `P4` | 168 |

#### Scenario: SLA is unaffected by the clarify override
- **GIVEN** a `bug` with `severity = high` and `has_reproduction_steps = false`
- **WHEN** routing runs
- **THEN** `queue = triage-clarify` and `sla_hours = 24`

#### Scenario: Popular low-severity enhancement
- **GIVEN** an `enhancement` with `severity = low` and 12 👍 reactions
- **WHEN** routing runs
- **THEN** its priority is `P3` and `sla_hours = 72`
