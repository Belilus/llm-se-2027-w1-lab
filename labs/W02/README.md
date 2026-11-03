# W2 lab — Reading, writing and composing specifications

Instructor's handout: `spec-lab/lab/README.md` (copied from
`llm-se-2027/W1/triage-spec-examples/` on 3 Nov 2026, commit `f574e50`). The instructor
updates his repo, so before each lab: `git -C ~/Documents/GitHub/llm-se-2027 pull --ff-only`
and compare with the copy here.

Everything for this lab lives in `spec-lab/`. It is a working copy of the instructor's
example folder, with `openspec init --tools none` already run. Write the answers in
`spec-lab/lab/worksheet.md`.

## What the lab asks (all three cycles use change request CR-1, `spec-lab/lab/change-request.md`)

| Cycle | Task | Edit / output |
|---|---|---|
| 1, track A | Translate CR-1 into the SRS and verify each requirement against ISO 29148 | `spec-lab/docs/srs-excerpt.md`, worksheet |
| 1, track B | Write the user stories for CR-1 (INVEST, Given/When/Then) and run the agent test | `spec-lab/docs/user-stories.md`, worksheet |
| 2 | Validate and archive `add-issue-triage`, then propose `add-security-queue` (do not archive it) | `spec-lab/openspec/`, worksheet |
| 3 | Add the two in-flight changes, route four issues R1–R4, draft glossary and invariants | `spec-lab/openspec/changes/`, worksheet |

Commands run from `labs/W02/spec-lab/` (the folder that holds `openspec/`).

## Syllabus brief (written before the handout was released)

> Reconstruct the requirements the W1 build implicitly assumed, as a use case and a user
> story with acceptance criteria. Classify each requirement and mark it verifiable or not,
> with justification.

Inputs: `../W01/decisions.md`, `../../src/triage/`, `../../src/triage_by_agent/`, notes in
`course-notes/שבועות/W02 דרישות ו-SDLC/`. Planned files, if this is still part of the
submission:

| File | Content |
|---|---|
| `use-case.md` | One use case: actor, goal, main flow, alternative flows |
| `user-story.md` | One user story (INVEST) with Given/When/Then acceptance criteria |
| `requirements.md` | Table: ID, requirement, type (FR / quality / constraint), verifiable? and why |
| `findings.md` | What was never specified, and what is unverifiable as written |
