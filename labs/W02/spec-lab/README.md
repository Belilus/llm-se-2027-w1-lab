# Running example: GitHub issue enrichment and routing — specification examples

Teaching material for *Software Engineering with AI*. Every document here describes the
**same** feature (the W1 lab triage pipeline), written in different specification styles so
students can compare what each style makes explicit and what it leaves out.

## The feature in one paragraph

Given a GitHub issue (title + body) from the frozen dataset (litestar-org/litestar,
honojs/hono, Textualize/textual), the system **enriches** it with structured triage fields
produced by an LLM (`issue_type`, `component`, `severity`, `has_reproduction_steps`,
`confidence`), **validates** them into a `TriageRecord`, and then **routes** the record
deterministically to a queue with an SLA and an escalation flag. Issue text is untrusted input.

## Contents

| File | Style | Use in class |
|---|---|---|
| `openspec/changes/add-issue-triage/proposal.md` | OpenSpec change proposal | Why / what changes / impact |
| `openspec/changes/add-issue-triage/specs/issue-enrichment/spec.md` | OpenSpec spec delta | Formal requirements + scenarios (LLM half) |
| `openspec/changes/add-issue-triage/specs/issue-routing/spec.md` | OpenSpec spec delta | Formal requirements + scenarios (deterministic half) |
| `openspec/changes/add-issue-triage/design.md` | OpenSpec design | Technical decisions, links to ADRs |
| `openspec/changes/add-issue-triage/tasks.md` | OpenSpec tasks | Implementation checklist for an agent |
| `docs/srs-excerpt.md` | IEEE/ISO/IEC 29148-style SRS | Classic requirements document, numbered IDs |
| `docs/user-stories.md` | User stories + acceptance criteria | Agile view, with traceability to the formal spec |
| `docs/adr/0001-…` – `0005-…` | Architecture Decision Records (Nygard/MADR) | Recording *why* |
| `exercises/flawed-spec.md` | Deliberately weak spec + stories | Critique exercise (student handout) |
| `exercises/flawed-spec-key.md` | Answer key | Instructor only |
| `lab/` | Hands-on lab (1 h 40): SRS vs stories, OpenSpec workflow, composing changes | Student handout + worksheet |

## Suggested discussion thread

1. Read the user stories first. What would a coding agent *still have to guess*?
2. Read the OpenSpec spec. Which of those guesses are now closed? Which remain?
3. Read the SRS excerpt. What does the numbered, exhaustive style buy you (traceability,
   auditability) and what does it cost (length, staleness)?
4. Read the ADRs. Which information appears in *none* of the specs, and why does it matter
   six months later?
5. Critique `exercises/flawed-spec.md`.

## Note on fidelity to `router.py`

The specs state the **intended** behaviour. One point deliberately differs from the current
lab code — see the open question in `design.md` (critical bugs without reproduction steps).
This makes a good "spec vs. implementation" discussion.
