# ADR-0004: Treat issue text as untrusted data

- **Status:** Accepted
- **Date:** 2026-10-27
- **Deciders:** Course staff
- **Related:** OpenSpec `issue-enrichment` (Untrusted Issue Text); SR-01…SR-03

## Context

Anyone with a GitHub account can open an issue. Real payloads appear in the wild: at least one
issue title in the frozen dataset (Textualize/textual) contains a shell command substitution
pointing at a bare IP address. Issue bodies can also contain text aimed at LLMs ("ignore
previous instructions…").

Two threats follow:

1. **Code execution** if issue text reaches a shell, `eval`, a file path, or a tool-enabled
   agent (including a coding agent working on the repository).
2. **Decision steering** if injected instructions change what the system does.

## Decision

- Issue text is data. It is never passed to a shell, interpolated into a command, used as a
  path, or given to a tool-enabled agent without a sandbox.
- The extraction model has **no tools**. Its only output channel is the five schema fields, and
  those are validated (ADR-0002) before routing sees them (ADR-0001).
- Raw issues are only ever written to disk as JSON.
- CI includes a grep check banning `subprocess`, `os.system`, `shell=True` and `eval` in
  `src/triage/`, and fixture issues with hostile titles and bodies.
- Students' coding agents must not be pointed at raw issue files with tool permissions enabled.

## Consequences

**Positive**
- The worst an injection can do is pick a different valid value for one of five fields. That
  risk is bounded and is mitigated further by escalation (ADR-0005).
- The threat model is explicit and testable.

**Negative**
- Injection can still bias classification (e.g. inflate severity). This is accepted and
  monitored, not prevented.
- Some convenient workflows (letting an agent "go read the issues and fix things") are
  disallowed.

## Alternatives considered

- **Sanitise issue text before use.** Rejected as the primary control: sanitisation is
  incomplete by nature. Containment by design is preferred.
