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
| FR-E-08 | Unambiguous, Complete | "Security label" is my assumption (name equals `security`, case-insensitive). Real repos use `Security`, `area/security`, `type: security`, `vulnerability`. Nothing says what to do when `labels` is missing or null. |
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
2. Which labels count as "the `security` label": exactly `security`, any case, or also
   `area/security`, `vulnerability`, `type: security` (the three repos label differently)? If the
   label is present and the model says "documentation", does the label win (my assumption: yes)?
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

| My format made explicit… | My partner's format made explicit… |
|---|---|
| | |

I would choose an SRS when …………………… and user stories when ……………………

---

## Cycle 2

**C1.** The error was: …………………… The change folder contained, but the main spec no longer
contains: ……………………

**C2.** Requirements in my delta:

| Capability | ADDED / MODIFIED | Requirement name |
|---|---|---|
| | | |

**C3.** A problem `validate` caught: …………………… A problem in my change that it **cannot** catch:
……………………

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
| R1 | | | | | |
| R2 | | | | | |
| R3 | | | | | |
| R4 | | | | | |

Other contradictions I found while reading the deltas: ……………………

### D3: domain model

**Glossary.** One sentence per term. In the last column, note where a term is used with
another meaning (which document or change).

| Term | Definition | Used differently in… |
|---|---|---|
| issue | | |
| triage record | | |
| component | | |
| queue | | |
| team / owner | | |
| severity | | |
| priority | | |
| critical | | |
| SLA | | |
| escalate | | |
| security issue | | |

**Invariants.** Rules that must hold *for every* issue, whatever feature is added later.

| # | Invariant ("for every …, …") | Catches problem(s)… |
|---|---|---|
| I1 | | |
| I2 | | |
| I3 | | |
| I4 | | |
| I5 | | |

Where would you put this so that (a) the next `/opsx:propose` reads it and (b) something
**checks** it automatically? ……………………
