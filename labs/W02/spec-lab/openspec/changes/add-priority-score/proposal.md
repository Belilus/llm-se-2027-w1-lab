# Change: Prioritise issues by community impact

*Author: Product team*

## Why

Severity is the model's estimate of technical impact. It ignores how many users are affected. A
medium-severity bug with 40 👍 reactions hurts more people than a high-severity bug nobody else
has hit, but today they get the same response deadline. Maintainers have asked for deadlines
that reflect community impact.

## What Changes

- **ADDED** requirement `Issue Priority`: every issue gets a priority from P1 (most urgent) to P4,
  computed from severity and the issue's 👍 reaction count.
- **MODIFIED** requirement `SLA by Severity`: the response deadline is now taken from priority
  instead of severity.
- The triage dashboard will show P1 issues as **critical issues**.

## Capabilities

### Modified Capabilities
- `issue-routing`

## Impact

- Affected code: `src/triage/router.py`, dashboard template
- No change to the model prompt or to the `TriageRecord` schema
