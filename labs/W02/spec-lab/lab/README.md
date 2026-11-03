# Lab: Reading, writing and composing specifications

*1 h 40. Hands-on. Uses the triage feature documents in this folder's parent directory.*

By the end of the lab you will have:

1. Read, edited and checked an **SRS** (ISO/IEC/IEEE 29148 style).
2. Read, edited and checked **user stories** with Given/When/Then acceptance criteria.
3. Compared the two formats and decided when each one is the better choice.
4. Taken a change through the **OpenSpec** workflow: validate → archive → propose → validate.
5. Seen why a set of separately valid changes can still produce an inconsistent system, and
   drafted the **domain model** that would have prevented it.

Write all your answers in [`worksheet.md`](worksheet.md), in your working copy.

## Before the lab (10 minutes, at home)

1. Install OpenSpec **1.16 or later**, with one of:
   `brew install openspec` · `npm install -g @fission-ai/openspec@latest` (needs Node ≥ 22.12) ·
   `curl -fsSL https://openspec.dev/cli/install.sh | sh`.
   Check it with `openspec --version`.
2. Download the example folder from the course repository. A sparse clone fetches only this folder, not the whole repository:

   ```bash
   cd ~
   git clone --depth 1 --filter=blob:none --sparse https://github.com/melhadad/llm-se-2027.git
   git -C llm-se-2027 sparse-checkout set W1/triage-spec-examples
   ```

   Then make your own working copy, with its own git history, and set up OpenSpec in it:

   ```bash
   cp -R ~/llm-se-2027/W1/triage-spec-examples ~/spec-lab
   cd ~/spec-lab
   git init -q && git add -A && git commit -qm "baseline"
   openspec init --tools none        # or: --tools claude / codex / cursor / github-copilot
   git add -A && git commit -qm "openspec init"
   ```

3. Read [`../README.md`](../README.md), the one-paragraph description of the feature.

## Schedule

| Time | Block |
|---|---|
| 0:00 | Introduction (lecturer) |
| 0:10 | **Cycle 1: SRS vs user stories.** 5' intro · 15' individual · 5' regroup |
| 0:35 | Tool check |
| 0:40 | **Cycle 2: OpenSpec workflow.** 5' intro · 15' individual · 5' regroup |
| 1:05 | **Cycle 3: Composing changes, and the domain model.** 5' intro · 15' individual · 5' regroup |
| 1:30 | Overflow for the cycle-3 discussion |
| 1:35 | Conclusion (lecturer) |

All three cycles use the same input: change request **CR-1** in
[`change-request.md`](change-request.md). Read it now. It takes 30 seconds.

---

## Cycle 1: SRS vs user stories (15 minutes, individual)

The class is split in two. **Track A** works on the SRS and **Track B** works on the user
stories. You will pair with someone from the other track in the regroup.

### Track A: SRS: [`../docs/srs-excerpt.md`](../docs/srs-excerpt.md)

| Step | Time | Task |
|---|---|---|
| A1 | 3' | **Read.** Skim §1.3, §3.2 and Appendix A. For **FR-R-05**, write down its verification method and the *one* test case (input → expected output) that verifies it most directly. |
| A2 | 8' | **Edit.** Translate CR-1 into SRS changes, directly in your copy of the file: new or changed rows in §3.1/§3.2 (with ID, priority and verification method), new §1.3 definitions, table changes, and Appendix A rows. If CR-1 forces an existing requirement to change, edit that requirement. Don't just add a new one beside it. |
| A3 | 4' | **Verify.** Check each requirement you added or changed against the 29148 characteristics (*necessary, unambiguous, singular, feasible, verifiable, consistent, complete*). In the worksheet, list every characteristic it fails and every question you would send back to the triage lead. |

### Track B: user stories: [`../docs/user-stories.md`](../docs/user-stories.md)

| Step | Time | Task |
|---|---|---|
| B1 | 3' | **Read.** Skim the stories. Rate **US-06** and **US-08** against INVEST (*Independent, Negotiable, Valuable, Estimable, Small, Testable*). Which letter is weakest for each? |
| B2 | 8' | **Edit.** Write the story or stories for CR-1 in your copy of the file, with role, goal, benefit, Given/When/Then acceptance criteria, size and *Traces to*. If your story fails INVEST because it is too big, split it. Update any existing story whose acceptance criteria CR-1 makes false. |
| B3 | 4' | **Verify.** Do the *agent test*: in the worksheet, list everything a coding agent would still have to **guess** to implement your stories. Also list the existing stories that interact with yours. |

---

## Cycle 2: OpenSpec workflow (15 minutes, individual)

Everyone does the same steps, in your working copy. Useful commands:

```text
openspec list [--specs]                    active changes, or current capabilities
openspec show <id> [--type spec]           display a change or a spec
openspec validate <id> --strict            check a change or spec
openspec archive <id> --yes                merge a change's deltas into openspec/specs/
openspec new change <id>                   create an empty change folder
openspec instructions <artifact> --change <id>   template + instructions (proposal, specs, …)
```

| Step | Time | Task |
|---|---|---|
| C1 | 4' | **Validate and archive the existing change.** Run `openspec validate add-issue-triage --strict`. It fails. Fix the **error** and run it again. Warnings remain, and `--strict` counts them as failures. That's expected; leave them. Then run `openspec archive add-issue-triage --yes` and `git diff --stat`. Open `openspec/specs/issue-routing/spec.md`. In the worksheet, write down what the change folder contained that the main spec no longer contains. |
| C2 | 8' | **Propose CR-1.** Run `openspec new change add-security-queue`. Write `proposal.md` (*Why / What Changes / Capabilities / Impact*) and one delta file per capability you touch, under `specs/<capability>/spec.md`. Use `## ADDED Requirements` for new requirements and `## MODIFIED Requirements` for changed ones. A MODIFIED block replaces the **whole** requirement, so copy it in full, then edit it. Every requirement needs at least one `#### Scenario:`. Reuse what you found in cycle 1. |
| C3 | 3' | **Validate.** Run `openspec validate add-security-queue --strict` until it passes. You can ignore a remaining *"Requirement text is very long"* warning. Then run `openspec show add-security-queue --json --deltas-only`. In the worksheet, write down one problem `validate` caught and one problem in your change that it **cannot** catch. **Do not archive.** |

*Finished early?* In a scratch copy, ask your coding agent `/opsx:propose` with the raw text of
CR-1. Diff its change against yours. What did the agent decide without asking you?

---

## Cycle 3: Composing changes, and the domain model (15 minutes, individual)

Two other teams have changes in flight against the same specs:
[`in-flight/add-priority-score`](in-flight/add-priority-score/) (Product team) and
[`in-flight/add-component-owners`](in-flight/add-component-owners/) (Platform team).

| Step | Time | Task |
|---|---|---|
| D1 | 2' | `cp -R lab/in-flight/* openspec/changes/`, then `openspec list` and `openspec validate --changes --strict`. All of them pass. Read the two proposals and their spec deltas. |
| D2 | 7' | **Route four issues.** Assume all three changes (theirs and yours) have been archived. Fill in the routing table in the worksheet for records R1–R4. For each cell, name the requirement that decides it. Write **?** where the specs don't determine the answer, contradict each other, or give an answer that depends on *when* routing runs. |
| D3 | 6' | **Draft the domain model** that would have prevented what you found in D2: a **glossary** (one definition per term, plus the terms that are used with two meanings), and 4–6 **invariants** of the form *"for every …, …"* that must hold whatever feature is added later. For each problem from D2, name the term or invariant that catches it. |

---

## Further reading

- OpenSpec docs: <https://openspec.dev/docs/glossary>
- ISO/IEC/IEEE 29148:2018 §5.2.5–5.2.6 (characteristics of individual requirements and of sets of requirements).
- B. Wake, *INVEST in Good Stories, and SMART Tasks* (2003).
- E. Evans, *Domain-Driven Design* (2003), ch. 2 *Communication and the Use of Language*.