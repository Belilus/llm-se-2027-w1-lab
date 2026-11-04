# Change: Route bugs to the owning team

*Author: Platform team*

## Why

The `engineering` queue for `honojs/hono` holds over 200 open bugs. Each team has to search it
for the bugs in the components it owns. Bugs should go straight to the team that owns the
affected component.

## What Changes

- **ADDED** requirement `Component Ownership`: a per-repository table, `config/owners.toml`,
  maps each component to the team that owns it.
- **MODIFIED** requirement `Queue by Issue Type`: a bug is assigned to its owning team's queue,
  `eng-<team>`. Bugs whose component has no owner stay in `engineering`.

## Capabilities

### Modified Capabilities
- `issue-routing`

## Impact

- Affected code: `src/triage/router.py`, new `config/owners.toml`
- New queues: one `eng-<team>` queue per team listed in `owners.toml`
- No change to enrichment
