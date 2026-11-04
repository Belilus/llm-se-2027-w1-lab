# Worksheet: specifications lab

Name: Asaf Belilus  Track (cycle 1): **A (SRS)** / ~~B (stories)~~

---

## Cycle 1

### Track A: SRS

**A1.** FR-R-05. Verification method: **Test** (Appendix A / §3.2 table says "Test"). The most direct
test case is the boundary of the confidence condition, because `iff` has to be checked in both
directions and `< 0.6` (not `≤`) is the only part of the rule that is easy to get wrong:

| Input record | Expected `escalate` |
|---|---|
| severity = high, confidence = 0.59 | **true** (the most direct case: both conditions of the second branch hold) |
| severity = high, confidence = 0.60 | false (boundary: `<` excludes 0.6) |
| severity = critical, confidence = 1.0 | true (first branch, confidence irrelevant) |
| severity = medium, confidence = 0.1 | false (the "only if" direction: low confidence alone does not escalate) |

*A2 (edit)*: done in `../docs/srs-excerpt.md`, version 0.4. New: FR-E-08, FR-E-09, FR-R-07,
FR-R-08, QR-05, Table 1 columns/rows, §1.3 definitions, Appendix A rows. Changed: FR-E-01,
FR-E-04, FR-R-02, FR-R-03, FR-R-04, FR-R-05, FR-R-06, Tables 2 and 3. See `git diff`.

**A3.** For each requirement you added or changed:

| ID | Fails which 29148 characteristic(s)? | Why |
|---|---|---|
| FR-E-01 (changed) | Singular | Two statements: what the enrichment input is, and that `labels` must not reach the model. The second follows from the first; it only stays so that FR-E-08 does not look like a contradiction. |
| FR-E-04 (changed) | Unambiguous (minor) | "Rows whose source is model" depends on a column that exists only because of CR-1; a reader of Table 1 alone would not know which output is checked. |
| FR-E-08 | Unambiguous, Complete | "Security label" is my assumption (name equals `security`, case-insensitive). In train and dev (960 issues) the only such label is `Security`, twice, both in litestar. hono and textual have none. CR-1 does not say if similar names should count. Nothing says what to do when `labels` is missing or null, but the field is present on all 960 issues. |
| FR-E-09 | none found | Singular, verifiable (a failure record either has the field or not). Necessary only if FR-R-07 applies to failures; that is question 5. |
| Table 1 `security_suspected` | Unambiguous, Verifiable | "True iff the issue is a security issue" rests on a judgement definition (§1.3). A crash that can be triggered remotely, a hardening idea and a pasted API key are all borderline. Verifiable only statistically (QR-05), so no single test case can say it is correct. |
| FR-R-05 (changed) | Singular | Three conditions in one requirement (the original had two). Testable, but a failing test does not say which branch broke. Also: CR-1 says "flagged to a human straight away", while escalation means "review before the SLA clock is acted on". "Straight away" is not verifiable, so I mapped it to `escalate = true`; the triage lead has to confirm that is enough. |
| FR-R-07 | Feasible (partly), Complete | The CR asks for a *private* queue. ITS is offline and emits a queue name only, so privacy cannot be enforced or tested here. I moved it out of scope in §1.2; the requirement now just routes to `security`. |
| FR-R-08 | Verifiable (partly) | "Handled within 24h" is a promise about humans. ITS can only emit `sla_hours`. The requirement tests the emitted number, not the real handling time. |
| QR-05 | Necessary, Feasible, Verifiable | The 0.95 target is invented by me, not asked for in CR-1. The held-out split may contain only a handful of security issues, so the recall estimate has a very wide interval. If the gold labels come from the GitHub `security` label, the metric is partly circular with `has_security_label`. |
| FR-R-02, FR-R-03, FR-R-04, FR-R-06 (changed) | none found (Consistent) | Only "except as in …" references added. Precedence is now stated once, in FR-R-07, so the four exceptions do not contradict. Readability gets worse with each exception. |

Existing requirements CR-1 forced me to change: **FR-E-01** (labels may now be read, though not
by the model), **FR-E-04** (Table 1 now has a column that is not model output), **FR-R-02**,
**FR-R-04** and **FR-R-06** (security takes precedence over type, over `triage-clarify` and over
`triage-manual`), **FR-R-03** (SLA cap), **FR-R-05** (a third escalation branch), and **Tables
1, 2, 3**. Not in the SRS but now also false: US-01's criterion "labels are not used" and the
OpenSpec scenario "Existing labels are ignored" (cycle 2 must modify `Enrichment Input
Contract`).

Questions for the triage lead:

1. What is a "security issue" at the edges: remotely triggerable crash/DoS, a hardening
   suggestion, a leaked key pasted into an issue, "is feature X safe to use?"? Is a missed
   vulnerability worse than a false alarm, and by how much (this sets the recall target in QR-05)?
2. Which labels count as "the `security` label": exactly `security`, any case, or also similar
   names such as `area/security` or `vulnerability`? In train and dev only `Security` appears,
   and only in litestar. If the label is present and the model says "documentation", does the
   label win (my assumption: yes)?
3. "Private queue" and "flagged to a human straight away": ITS is an offline batch with no
   write-back. Is the queue name plus `escalate = true` in the output JSON all ITS must do, with
   access control and notification handled downstream? Who is the downstream system?
4. "Handled within 24h max": is that a cap on the emitted SLA (my reading) or a target for real
   response time? Should critical-severity security issues keep the 4 h SLA?
5. When enrichment fails twice and the issue has the security label, route to `security` (my
   assumption). When it fails and has no label, a real vulnerability waits in `triage-manual`
   for 72 h, the same failure as last week. Is that acceptable, or should failures be escalated?
6. Do the datasets have gold security labels, how many are in the held-out split, and where do
   they come from? Without that, QR-05 cannot be measured.

### Track B: user stories

**B1.** Weakest INVEST letter for US-06: … because … · for US-08: … because …

**B3.** What a coding agent would still have to guess:

1.
2.
3.

Existing stories that interact with yours: ……………………

### Regroup: compare with your partner from the other track

I did not have a partner from track B, so this is not a real comparison. The right column comes
from my own reading of `docs/user-stories.md`, and I did not write stories for CR-1.

| My format made explicit… | My partner's format made explicit… |
|---|---|
| Definitions in one place (§1.3), the exceptions between requirements (FR-R-07 over FR-R-02, FR-R-04 and FR-R-06), what is out of scope (access control on queues), and how each requirement is verified. | Who needs each thing and why, concrete examples with boundaries (confidence exactly 0.6 is not escalated), and the size of the work. Stories also have a Security reviewer role that the SRS user classes do not have. |

I would choose an SRS when the rules have to hold together and be verified one by one, like the
routing policy with its exceptions in CR-1, and user stories when the main question is who needs
what and why, and the team wants to plan the work in small pieces with concrete examples.

---

## Cycle 2

**C1.** The error was: `issue-routing/spec.md: ADDED "Routing Result" must include at least
one scenario`. I added the scenario "All result fields are present" to that requirement. The
error went away. The three warnings stayed, as the handout expected, so `--strict` still exits
with 1.

The change folder contained, but the main spec no longer contains:

- `proposal.md`: why we made the change, what is out of scope, and the impact.
- `design.md`: the pipeline, the decisions, the risks and the open questions.
- `tasks.md`: 22 tasks, all still unchecked. The archive warned about this and continued
  because of `--yes`.
- Both "Non-functional requirements (informative)" sections. Routing lost testability and
  exhaustiveness. Enrichment lost type safety, reproducibility and the quality targets (macro-F1
  ≥ 0.75, severity within-one-level agreement ≥ 0.85). The archive warned about this too.

These files still exist under `openspec/changes/archive/2026-11-04-add-issue-triage/`, but the
main spec does not show them. So the main spec keeps the behavior and loses the reasons and the
targets. One leftover: the note under the Escalation requirement was carried over and still says
"See the open question in `design.md`", and that file is no longer next to the spec. The new
spec also has a placeholder Purpose ("TBD"). `git diff --stat` shows only 344 deletions, because
the new spec files and the archive folder are still untracked.

**C2.** Requirements in my delta:

| Capability | ADDED / MODIFIED | Requirement name |
|---|---|---|
| `issue-enrichment` | ADDED | Security Label Signal |
| `issue-enrichment` | ADDED | Security Issue Detection |
| `issue-enrichment` | ADDED | Security Recall |
| `issue-enrichment` | MODIFIED | Enrichment Input Contract |
| `issue-enrichment` | MODIFIED | Triage Record Schema |
| `issue-enrichment` | MODIFIED | Bounded Retry and Explicit Failure |
| `issue-enrichment` | MODIFIED | Untrusted Issue Text |
| `issue-routing` | ADDED | Security Queue |
| `issue-routing` | MODIFIED | SLA by Severity |
| `issue-routing` | MODIFIED | Clarification Queue for Unreproducible Bugs |
| `issue-routing` | MODIFIED | Escalation |
| `issue-routing` | MODIFIED | Enrichment Failures are Routed |

`Untrusted Issue Text` was not in my SRS work. Its scenario says the injected text has "the five
model-produced fields" as its only channel, and `security_suspected` makes that six. `Queue by
Issue Type` did not need a change, because it already says "unless another requirement in this
spec overrides it".

**C3.** A problem `validate` caught: I renamed the scenario "Existing labels are ignored" in the
MODIFIED `Enrichment Input Contract`, and it failed with `omits scenario(s) the current spec still
has`, because a MODIFIED block must not silently drop a scenario. I put the old name back.

A problem in my change that it **cannot** catch: `validate` checks structure and not meaning.
An issue with a failed enrichment and no security label still goes to `triage-manual` for 72
hours, so a real vulnerability can still wait in the way CR-1 complains about. The change is valid
anyway. To check this, I changed a scenario in a scratch copy to `sla_hours = 500`,
`escalate = false`, which contradicts its own requirement, and `validate` still passed. It also
cannot tell if "private" is true, if the 0.95 recall target makes sense, or if gold security
labels exist at all.

---

## Cycle 3

### D2: route four issues, assuming all three changes have been archived

| | Record |
|---|---|
| **R1** | `honojs/hono` · `bug` · `component = "router"` · `severity = critical` · no reproduction steps · `confidence = 0.9` · flagged as a security report · 3 👍 |
| **R2** | `Textualize/textual` · `question` · `severity = high` · `confidence = 0.55` · not security · 8 👍 when first triaged, 40 👍 today |
| **R3** | `honojs/hono` · `bug` · `component = "Routing"` (the model's words) · `severity = high` · has reproduction steps · `confidence = 0.8` · not security · 2 👍. `owners.toml` maps (`honojs/hono`, `router`) → `core`. |
| **R4** | `litestar-org/litestar` · **`TriageFailure`** (both model outputs invalid) · a maintainer has added the `security` label · 50 👍 |

| | `queue` | `sla_hours` | `escalate` | Requirement(s) that decide it | **?** and why |
|---|---|---|---|---|---|
| R1 | `security` | 4 | true | Queue: Security Queue, which overrides the type queue and `triage-clarify`. SLA: critical gives 4 by severity, P1 gives 4 by priority. Escalate: Escalation (critical, and security-flagged). | The values are decided, but only because Security Queue states its override. `add-component-owners` removed "unless another requirement overrides it" from Queue by Issue Type, so read alone that requirement says `eng-core`. |
| R2 | `support` | **?** 24 or 4 | true | Queue: Queue by Issue Type. SLA: Issue Priority and SLA by Severity. Escalate: Escalation (high and 0.55 < 0.6). | **Depends on when routing runs.** 8 👍 gives P2 and 24 hours. 40 👍 gives P1 and 4 hours. Deterministic Routing says no I/O and equal inputs give equal outputs, but 👍 is not in `TriageRecord`, and task 1.1 fetches it inside `route()`. |
| R3 | **?** `engineering` or `eng-core` | 24 | false | Queue: Component Ownership and Queue by Issue Type. SLA: high gives 24 by severity, P2 gives 24 by priority. Escalate: Escalation (high, but 0.8 is not < 0.6). | **Not determined.** `component` is free text from the model and the key in `owners.toml` is `router`. Nothing says how names are matched. An exact match finds no owner and gives `engineering`. A normalized match gives `eng-core`. `design.md` deferred this as open question 2. |
| R4 | **?** `security` | **?** 24 | **?** true | Queue, SLA and escalate: Enrichment Failures are Routed and Security Queue, if the label was there when the run happened. | **Depends on when, and contradiction.** `has_security_label` is read at enrichment. If the maintainer added the label after that, the failure has it as false and the answer is `triage-manual`, 72, false. Also, Issue Priority says each issue gets a priority from severity, but a `TriageFailure` has no severity, so the 50 👍 fit no row. The priority version of the SLA has no case for failures. |

Other contradictions I found while reading the deltas:

1. **Two changes replace the same requirement.** `add-security-queue` and `add-priority-score` both
   MODIFY SLA by Severity. All three changes pass `openspec validate --changes --strict`, but in a
   scratch copy the archive refused whichever of the two came second, in both orders ("Refresh the
   change spec before archiving to avoid dropping scenarios"). So "all three archived" cannot
   happen until someone merges them by hand. If the cap gets lost in that merge, a medium security
   issue with fewer than 10 👍 gets P3 and 72 hours instead of 24.
2. **A removed exception that nothing reports.** `add-component-owners` archived with no complaint
   in both orders, and the sentence "unless another requirement overrides it" was gone.
3. **"Critical" has two meanings.** `add-priority-score` shows P1 issues on the dashboard as
   critical issues. A high issue with 10 👍 or more is P1, but Escalation looks at
   `severity = critical`. With confidence of 0.6 or more, the dashboard says critical and
   `escalate` is false.
4. **The name no longer fits.** SLA by Severity would be decided by priority.
5. **The proposal and the spec disagree.** `add-priority-score` says there is no change to the
   `TriageRecord` schema, but routing is a pure function of that record and needs the 👍 count.

### D3: domain model

**Glossary.** One sentence per term. In the last column, note where a term is used with
another meaning (which document or change).

| Term | Definition | Used differently in… |
|---|---|---|
| issue | A GitHub issue, identified by `repo` and `issue_number`, as it was when it was triaged. | `add-priority-score` says "each issue" gets a priority from severity, but an issue that ends in a `TriageFailure` has no severity. |
| triage record | The validated, immutable result of a successful enrichment. It holds everything routing is allowed to read. | The SRS says "failure record" and the specs say `TriageFailure`. `add-priority-score` needs the 👍 count, which is not in the record. |
| component | The part of a repository that an issue affects, as one name from that repository's list, or null. | In `TriageRecord` it is free text from the model. In `owners.toml` it is an exact key. `config/repos.toml` has a third per-repo list. |
| queue | The named destination that routing emits for one issue. | CR-1 treats a queue as public or private, but the SRS and specs treat it as only a name. `add-component-owners` turns `engineering` into many `eng-<team>` queues. |
| team / owner | The one group of people responsible for a component in a repository. | `add-component-owners` uses team for a name in `owners.toml`. The other documents talk about a maintainer who works a queue, and the SRS has no team at all. |
| severity | The model's estimate of the technical impact of an issue: low, medium, high or critical. | `add-priority-score` keeps this meaning but stops using it directly for the deadline. There are no gold labels, so nothing measures it. |
| priority | Urgency from P1 to P4, computed from severity and the 👍 count at one recorded moment. | It exists only in `add-priority-score`, and it does not say which moment. It is not defined for a `TriageFailure`. |
| critical | Only the value `severity = critical`. | `add-priority-score` shows every P1 issue as a critical issue on the dashboard, and a P1 can have `severity = high`. |
| SLA | The response deadline in hours that routing emits (`sla_hours`). It is a number in the output and not a measure of what people do. | CR-1 says "handled within 24h". The stories say "response deadline". The requirement SLA by Severity would be decided by priority. |
| escalate | A flag saying that a human must review the issue before the SLA is acted on. | CR-1 says "flagged to a human straight away", which is a time promise. The system only emits a boolean. |
| security issue | An issue that reports a vulnerability or discloses a secret (SRS §1.3). A security-flagged issue is one the model suspects or one with a security label. | CR-1 says "security stuff". The specs route on security-flagged, which is a signal and not proof. A label can mark an issue that is not a real security issue, and the model can miss a real one. |

**Invariants.** Rules that must hold *for every* issue, whatever feature is added later.

| # | Invariant ("for every …, …") | Catches problem(s)… |
|---|---|---|
| I1 | For every issue in a run, there is exactly one outcome, a triage record or a `TriageFailure`, and routing gives it exactly one queue, one `sla_hours` and one `escalate`. | R4: a failure has no severity, so it has no priority and no SLA from the priority table. |
| I2 | For every routing result, every value that routing used is stored in the record it read, so routing the same record twice at any time gives the same result. | R2: the 👍 count changes over time. R4: the label may be added after enrichment. Contradiction 5: 👍 is not in `TriageRecord`. |
| I3 | For every security-flagged issue, `queue = security`, `escalate = true` and `sla_hours` ≤ 24, whatever other rule also matches. | R1: the override in Queue by Issue Type was removed. Contradiction 1: the 24 hour cap can get lost in the merge. Contradiction 2: the removed exception. |
| I4 | For every value used as a lookup key, the value comes from a fixed per-repo list, or it is null, and it is never raw model text. | R3: `"Routing"` does not match `router`. |
| I5 | For every issue shown or reported as critical, `severity = critical`, and for every issue with `severity = critical`, `escalate = true`. | Contradiction 3: a P1 with `severity = high` is shown as critical and is not escalated. |

Contradiction 4 is caught by the glossary term **SLA**: the term does not depend on how the
number is computed, so a requirement name should not tie it to severity or priority.

Where would you put this so that (a) the next `/opsx:propose` reads it and (b) something
**checks** it automatically?

(a) In `openspec/config.yaml`, under `context:`. I tested this on a scratch copy: the text shows
up in the output of `openspec instructions proposal` and `openspec instructions specs`, inside
`<project_context>`. That is what the agent gets when it writes a proposal.

(b) As property-based tests in `tests/`, run with `uv run pytest` before every merge. They generate
records and failures, including security-flagged ones, and assert I1 to I5 on the routing output.
`openspec validate` cannot do this, because it checks structure and not meaning (see C3). These
tests do not exist yet, and I4 also needs a check that `owners.toml` keys are in the per-repo list.
