# Software Requirements Specification — Issue Triage (excerpt)

*Structure follows ISO/IEC/IEEE 29148:2018, §9.6. Excerpt only: sections 1–3 abbreviated,
selected requirements shown.*

| Field | Value |
|---|---|
| Document ID | SRS-TRIAGE-001 |
| Version | 0.3 (draft) |
| Status | For review |
| Related | OpenSpec change `add-issue-triage`; ADR-0001…0005 |

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for the Issue Triage System (ITS), which enriches
GitHub issues with structured triage attributes and routes them to work queues.

### 1.2 Scope
ITS operates offline over a frozen dataset of issues from three public repositories. Live
ingestion and write-back to GitHub are excluded.

### 1.3 Definitions
| Term | Definition |
|---|---|
| Enrichment | Derivation of triage attributes from issue text by a language model |
| Triage record | Validated, immutable set of triage attributes for one issue |
| Routing | Deterministic mapping from a triage record to queue, SLA and escalation flag |
| Escalation | Flag indicating that a human maintainer must review the issue before the SLA clock is acted on |

## 2. Overall description

### 2.1 Product perspective
ITS is a batch component. Inputs: issue JSON files. Outputs: one result JSON per issue and an
evaluation report.

### 2.2 User classes
| Class | Need |
|---|---|
| Maintainer | Receives routed issues; needs correct queue and urgency |
| Triage lead | Owns routing policy; needs rules to be inspectable and changeable |
| Evaluator | Measures enrichment quality against gold labels |

### 2.3 Constraints
- C-1 Python 3.13; dependency management with `uv`.
- C-2 Static type checking with pyright in strict mode.
- C-3 Issue text is untrusted (see §3.4).

## 3. Specific requirements

### 3.1 Functional — enrichment

| ID | Requirement | Priority | Verification |
|---|---|---|---|
| FR-E-01 | ITS shall use only `title` and `body` of an issue as enrichment input. | Must | Test |
| FR-E-02 | ITS shall produce a triage record with the attributes defined in Table 1. | Must | Test |
| FR-E-03 | ITS shall copy `repo` and `issue_number` from the input, not from model output. | Must | Test |
| FR-E-04 | ITS shall reject any model output that does not satisfy Table 1, without coercion. | Must | Test |
| FR-E-05 | ITS shall retry enrichment at most once after a rejected output. | Should | Test |
| FR-E-06 | ITS shall emit a failure record after two rejected outputs and continue the batch. | Must | Test |
| FR-E-07 | ITS shall record the model identifier in every output. | Must | Inspection |

**Table 1 — Triage record attributes**

| Attribute | Domain |
|---|---|
| `issue_type` | {bug, enhancement, documentation, question, meta} |
| `component` | free text or null |
| `severity` | {low, medium, high, critical} |
| `has_reproduction_steps` | boolean |
| `confidence` | real, [0.0, 1.0] |

### 3.2 Functional — routing

| ID | Requirement | Priority | Verification |
|---|---|---|---|
| FR-R-01 | Routing shall depend only on the triage record and static tables. | Must | Test, Inspection |
| FR-R-02 | The queue shall be selected by `issue_type` per Table 2, except as in FR-R-04. | Must | Test |
| FR-R-03 | The SLA shall be selected by `severity` per Table 3. | Must | Test |
| FR-R-04 | A bug without reproduction steps shall be routed to `triage-clarify`. | Must | Test |
| FR-R-05 | Escalation shall be set iff severity is critical, or severity is high and confidence < 0.6. | Must | Test |
| FR-R-06 | A failure record shall be routed to `triage-manual` with a 72-hour SLA. | Must | Test |

**Table 2 — Queue by type:** bug → engineering; enhancement → product;
documentation → docs; question → support; meta → maintainers.

**Table 3 — SLA by severity:** critical → 4 h; high → 24 h; medium → 72 h; low → 168 h.

### 3.3 Quality requirements

| ID | Requirement | Verification |
|---|---|---|
| QR-01 | `issue_type` macro-F1 on the held-out split shall be ≥ 0.75. | Analysis |
| QR-02 | `severity` within-one-level agreement on the held-out split shall be ≥ 0.85. | Analysis |
| QR-03 | The package shall report zero pyright strict errors. | Test |
| QR-04 | Re-running with the same model identifier and response cache shall produce identical outputs. | Test |

### 3.4 Security requirements

| ID | Requirement | Verification |
|---|---|---|
| SR-01 | Issue text shall not be passed to a shell, interpolated into a command, or used as a path. | Inspection, Test |
| SR-02 | Issue text shall not be provided to any tool-enabled agent. | Inspection |
| SR-03 | Only validated record attributes shall influence routing. | Test |

## Appendix A. Traceability (excerpt)

| SRS ID | OpenSpec requirement | User story |
|---|---|---|
| FR-E-01 | Enrichment Input Contract | US-01 |
| FR-E-04 | Validation at the Model Boundary | US-02 |
| FR-E-06 | Bounded Retry and Explicit Failure | US-03 |
| FR-R-04 | Clarification Queue for Unreproducible Bugs | US-05 |
| FR-R-05 | Escalation | US-06 |
| SR-01 | Untrusted Issue Text | US-08 |
