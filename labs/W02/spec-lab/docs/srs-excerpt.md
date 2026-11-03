# Software Requirements Specification — Issue Triage (excerpt)

*Structure follows ISO/IEC/IEEE 29148:2018, §9.6. Excerpt only: sections 1–3 abbreviated,
selected requirements shown.*

| Field | Value |
|---|---|
| Document ID | SRS-TRIAGE-001 |
| Version | 0.4 (draft) |
| Status | For review |
| Related | OpenSpec change `add-issue-triage`; ADR-0001…0005; CR-1 (OpenSpec change `add-security-queue`) |
| Changes in 0.4 | CR-1: security queue. New: FR-E-08, FR-E-09, FR-R-07, FR-R-08, QR-05. Changed: FR-E-01, FR-E-04, FR-R-02, FR-R-03, FR-R-04, FR-R-05, FR-R-06, Table 1, Table 2, Table 3. |

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for the Issue Triage System (ITS), which enriches
GitHub issues with structured triage attributes and routes them to work queues.

### 1.2 Scope
ITS operates offline over a frozen dataset of issues from three public repositories. Live
ingestion and write-back to GitHub are excluded. Access control on queues is excluded: ITS
only emits the queue name, and keeping the `security` queue private is the responsibility of
whatever system consumes the output.

### 1.3 Definitions
| Term | Definition |
|---|---|
| Enrichment | Derivation of triage attributes from issue text by a language model |
| Triage record | Validated, immutable set of triage attributes for one issue |
| Routing | Deterministic mapping from a triage record to queue, SLA and escalation flag |
| Escalation | Flag indicating that a human maintainer must review the issue before the SLA clock is acted on |
| Security issue | An issue whose `title` or `body` reports a vulnerability (a weakness that can be exploited to breach confidentiality, integrity or availability) or discloses a secret such as a credential or key. A request for a security feature, or a question about configuring security, is not a security issue |
| Security label | A GitHub label on the issue whose name equals `security`, compared case-insensitively |
| Security-flagged | Property of an issue: the model judged it a security issue (`security_suspected` is true in its triage record), or it carries a security label (`has_security_label` is true in its triage record or failure record) |

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
| FR-E-01 | ITS shall use only `title` and `body` of an issue as enrichment input. The `labels` field shall not be provided to the model. | Must | Test |
| FR-E-02 | ITS shall produce a triage record with the attributes defined in Table 1. | Must | Test |
| FR-E-03 | ITS shall copy `repo` and `issue_number` from the input, not from model output. | Must | Test |
| FR-E-04 | ITS shall reject any model output that does not satisfy the rows of Table 1 whose source is "model", without coercion. | Must | Test |
| FR-E-05 | ITS shall retry enrichment at most once after a rejected output. | Should | Test |
| FR-E-06 | ITS shall emit a failure record after two rejected outputs and continue the batch. | Must | Test |
| FR-E-07 | ITS shall record the model identifier in every output. | Must | Inspection |
| FR-E-08 | ITS shall set `has_security_label` to true if and only if the input issue carries a security label, without involving the model. | Must | Test |
| FR-E-09 | ITS shall include `has_security_label` in every failure record. | Must | Test |

**Table 1 — Triage record attributes**

| Attribute | Domain | Source |
|---|---|---|
| `issue_type` | {bug, enhancement, documentation, question, meta} | model |
| `component` | free text or null | model |
| `severity` | {low, medium, high, critical} | model |
| `has_reproduction_steps` | boolean | model |
| `confidence` | real, [0.0, 1.0] | model |
| `security_suspected` | boolean; true iff the issue is a security issue | model |
| `has_security_label` | boolean | input `labels` (FR-E-08) |

### 3.2 Functional — routing

| ID | Requirement | Priority | Verification |
|---|---|---|---|
| FR-R-01 | Routing shall depend only on the triage record and static tables. | Must | Test, Inspection |
| FR-R-02 | The queue shall be selected by `issue_type` per Table 2, except as in FR-R-04 and FR-R-07. | Must | Test |
| FR-R-03 | The SLA shall be selected by `severity` per Table 3, except as in FR-R-08. | Must | Test |
| FR-R-04 | A bug without reproduction steps shall be routed to `triage-clarify`, except as in FR-R-07. | Must | Test |
| FR-R-05 | Escalation shall be set iff (a) severity is critical, or (b) severity is high and confidence < 0.6, or (c) the issue is security-flagged. | Must | Test |
| FR-R-06 | A failure record shall be routed to `triage-manual` with a 72-hour SLA, except as in FR-R-07 and FR-R-08. | Must | Test |
| FR-R-07 | A security-flagged issue, whether it has a triage record or a failure record, shall be routed to the `security` queue. This takes precedence over FR-R-02, FR-R-04 and FR-R-06. | Must | Test |
| FR-R-08 | The SLA of a security-flagged issue shall be the lesser of 24 hours and the SLA that FR-R-03 or FR-R-06 would otherwise select. | Must | Test |

**Table 2 — Queue by type:** bug → engineering; enhancement → product;
documentation → docs; question → support; meta → maintainers. A security-flagged issue goes
to `security` regardless of type (FR-R-07).

**Table 3 — SLA by severity:** critical → 4 h; high → 24 h; medium → 72 h; low → 168 h. For a
security-flagged issue the value is capped at 24 h (FR-R-08).

### 3.3 Quality requirements

| ID | Requirement | Verification |
|---|---|---|
| QR-01 | `issue_type` macro-F1 on the held-out split shall be ≥ 0.75. | Analysis |
| QR-02 | `severity` within-one-level agreement on the held-out split shall be ≥ 0.85. | Analysis |
| QR-03 | The package shall report zero pyright strict errors. | Test |
| QR-04 | Re-running with the same model identifier and response cache shall produce identical outputs. | Test |
| QR-05 | `security_suspected` recall on the held-out split, against gold security labels, shall be ≥ 0.95. Threshold proposed, to be confirmed by the triage lead. | Analysis |

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
| FR-E-08 | Security Label Signal (new, `add-security-queue`) | to be written (track B) |
| FR-E-09 | Bounded Retry and Explicit Failure (modified) | to be written (track B) |
| FR-R-03 | SLA by Severity (modified) | to be written (track B) |
| FR-R-04 | Clarification Queue for Unreproducible Bugs | US-05 |
| FR-R-05 | Escalation | US-06 |
| FR-R-07 | Security Queue (new) | to be written (track B) |
| FR-R-08 | SLA by Severity (modified) | to be written (track B) |
| QR-05 | Security Recall (new) | to be written (track B) |
| SR-01 | Untrusted Issue Text | US-08 |
