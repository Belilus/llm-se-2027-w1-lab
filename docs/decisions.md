# Unspecified decisions

The brief did not tell you everything. Every time you or your agent chose
something the brief did not specify, add a line here.

Examples of the kind of thing that counts: what fields the record has, what
happens to an issue with no clear type, how confident is confident enough,
what the output looks like when the model returns nothing usable.

You will need this list in W2, when we reconstruct the requirements this
build implicitly assumed. The comparison across the cohort is the lesson, so
write down what you actually decided, not what you think is the right answer.

---

- Record fields: `repo`, `number`, `issue_type`, `component`, `severity`, `has_reproduction_steps`, `confidence`, `summary`, `model`.
- `issue_type` is a closed enum `bug | enhancement | documentation | question | meta` (taken from `config/repos.toml`); there is no "other"/"unknown" type, so an unclear issue must still pick one.
- `severity` is a 4-level enum `low | medium | high | critical`; "critical" means outage, data loss or security hole. No gold labels exist for it, so the scale is my own.
- `component` is free text (lowercase, ≤ 40 chars), not the per-repo taxonomy; the model's `unknown` becomes `null`.
- `confidence` is a float in [0, 1], self-reported by the model and only about `issue_type`; it is not calibrated and nothing uses it yet.
- Input is title + body only. Labels and comments are never shown to the model (labels are where gold labels come from; comments do not exist when a new issue arrives).
- The body is truncated to 8,000 characters before it is sent to the model.
- `repo` and `number` are copied from the input, never from the model output.
- Model output is never coerced: an out-of-range confidence or a label outside the enum is rejected, not clamped or mapped.
- On invalid output or a failed call: retry once, then emit a `TriageFailure` (reason + raw output ≤ 2,000 chars) instead of raising. A batch keeps going.
- The retry is immediate (no backoff), so it does not help with rate limits (see review-findings, surprise 1).
- Model chosen by the `LLM_MODEL` env var (default `gemini/gemini-3.5-flash-lite`), temperature 0, max 400 output tokens; the model id is recorded in every record.
- Output is one JSON object per line on stdout; exit code 2 if any issue failed.
- The CLI refuses the sealed `test` split.
- Added a one-sentence `summary` field (≤ 200 chars) for a human reading the queue — it is a free-text channel that issue text can influence.

## Where my `src/triage/` and the released `src/triage_by_agent/` differ

(fill in after Exercise B)
