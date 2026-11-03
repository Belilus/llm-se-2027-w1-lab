# ADR-0001: Separate LLM extraction from deterministic routing

- **Status:** Accepted
- **Date:** 2026-10-27
- **Deciders:** Course staff
- **Related:** OpenSpec `issue-routing` (Deterministic Routing); ADR-0002, ADR-0005

## Context

Triage involves two different kinds of judgement:

1. *Reading* an issue to decide what it is about and how bad it sounds. This is fuzzy and
   language-dependent, and an LLM is a reasonable tool for it.
2. *Deciding what to do* given that reading: which queue, which deadline, whether to escalate.
   This is organisational policy. It must be explainable, auditable and changeable by the
   triage lead without touching a model.

A single prompt such as "read this issue and tell me which queue it goes to" would be shorter to
write, but it would merge the two, so a policy change would become a prompt change, and every
routing decision would carry model uncertainty.

## Decision

The pipeline is split into two stages joined by a typed record:

- `extract.py` asks the model for **attributes only** (`issue_type`, `component`, `severity`,
  `has_reproduction_steps`, `confidence`). It never asks for a queue, SLA or escalation.
- `router.py` is a pure function `TriageRecord → Routing` with static tables. It makes no
  model calls, ever.

## Consequences

**Positive**
- Routing is unit-testable to 100% of its rules; it is correct or incorrect, not "87% accurate".
- Policy changes (new queue, new SLA) are code changes reviewed like any other.
- Model upgrades cannot change policy; they can only change attribute quality, which is
  measured separately.

**Negative**
- The model cannot use context that the five attributes don't capture (e.g. "this is clearly
  for the CLI team"). Adding such signals requires a schema change.
- Two components to maintain instead of one prompt.

## Alternatives considered

- **End-to-end prompt that outputs the queue.** Rejected: untestable policy, prompt-coupled.
- **Model proposes a queue, rules veto it.** Rejected for now: adds a reconciliation step whose
  failure modes are hard to specify. May revisit if the attribute set proves too thin.
