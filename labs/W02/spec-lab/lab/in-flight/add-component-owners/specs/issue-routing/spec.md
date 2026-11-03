# Spec delta: issue-routing

## ADDED Requirements

### Requirement: Component Ownership
The system SHALL read component ownership from `config/owners.toml`, which maps a pair
(`repo`, component name) to a team name. A component SHALL have at most one owning team.

#### Scenario: Owned component
- **GIVEN** `owners.toml` maps (`honojs/hono`, `router`) to team `core`
- **WHEN** the owner of component `router` in `honojs/hono` is looked up
- **THEN** the owner is `core`

#### Scenario: Unowned component
- **GIVEN** `owners.toml` has no entry for (`honojs/hono`, `jsx`)
- **WHEN** the owner of component `jsx` in `honojs/hono` is looked up
- **THEN** there is no owner

## MODIFIED Requirements

### Requirement: Queue by Issue Type
The queue SHALL be determined by `issue_type`:

| `issue_type` | `queue` |
|---|---|
| `bug` | `eng-<team>`, where `<team>` owns the issue's component; `engineering` if no team owns it |
| `enhancement` | `product` |
| `documentation` | `docs` |
| `question` | `support` |
| `meta` | `maintainers` |

#### Scenario: Bug in an owned component
- **GIVEN** a `bug` in `honojs/hono` with `component = "router"`, and `router` is owned by `core`
- **WHEN** routing runs
- **THEN** `queue = eng-core`

#### Scenario: Bug in an unowned component
- **GIVEN** a `bug` in `honojs/hono` with `component = "jsx"`, and `jsx` has no owner
- **WHEN** routing runs
- **THEN** `queue = engineering`

#### Scenario: Enhancement
- **GIVEN** a record with `issue_type = enhancement`, `severity = low`
- **WHEN** routing runs
- **THEN** `queue = product`
