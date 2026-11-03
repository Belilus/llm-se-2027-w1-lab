# ADR-0003: Use DSPy signatures for extraction instead of hand-written prompts

- **Status:** Accepted
- **Date:** 2026-10-27
- **Deciders:** Course staff
- **Related:** OpenSpec `issue-enrichment` (Model Configuration); QR-01, QR-02

## Context

The extraction step could be implemented as a hand-written prompt template plus a JSON parser,
or with a framework that declares inputs and outputs and generates the prompt. Three forces:

- The model identifier must be swappable (`LLM_MODEL`) and results compared across models.
- We want to evaluate and later optimise extraction against gold labels.
- Students should see the interface (fields and descriptions) rather than prompt wording.

## Decision

Extraction is a DSPy `Signature` (`TriageSignature`) with two inputs (`title`, `body`) and five
output fields with short descriptions, executed via `dspy.Predict`. The model is configured
from `LLM_MODEL`. Prompt text is not committed by hand.

## Consequences

**Positive**
- The signature reads as a typed interface and maps one-to-one to `TriageRecord`.
- Model swaps are configuration, not code.
- Opens a path to DSPy optimisers (few-shot selection) against the dev split.

**Negative**
- DSPy output fields are strings; typing still has to be enforced by ADR-0002.
- An additional dependency with its own release cadence; generated prompts are less
  transparent than a hand-written template.
- Debugging requires inspecting DSPy's prompt history.

## Alternatives considered

- **Hand-written prompt + `json.loads`.** Simpler, fully transparent; rejected because model
  comparison and optimisation would be ad hoc.
- **Provider structured-output APIs directly.** Couples the code to one provider.
