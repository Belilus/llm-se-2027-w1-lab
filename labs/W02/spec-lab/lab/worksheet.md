# Worksheet: specifications lab

Name: ……………………  Track (cycle 1): **A (SRS)** / **B (stories)**

---

## Cycle 1

### Track A: SRS

**A1.** FR-R-05. Verification method: ……… Test case:

| Input record | Expected `escalate` |
|---|---|
| | |

**A3.** For each requirement you added or changed:

| ID | Fails which 29148 characteristic(s)? | Why |
|---|---|---|
| | | |

Existing requirements CR-1 forced you to change: ……………………

Questions for the triage lead:

1.
2.
3.

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
