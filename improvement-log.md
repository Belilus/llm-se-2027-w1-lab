# Improvement log

Every time the agent gets something wrong, it goes here. Not the fix — the
*failure*, classified.

This file runs for the whole semester. In W12 you will use it to show what
changed about how you work. That only works if it was written as things
happened, so write entries the day they occur. An improvement log
reconstructed from memory in week eleven is a creative writing exercise.

## The taxonomy

Classify every entry as exactly one of:

| Class | Meaning | Where the fix usually belongs |
|---|---|---|
| `capability` | the model could not do this | change the task, or the model |
| `context` | it could have, but did not know something | what the agent is given to read |
| `tool` | it lacked a way to act or to check | tooling |
| `spec` | the request was ambiguous and it guessed | the specification |
| `concept` | it used the wrong idea or the wrong name | the domain model |
| `bug` | ordinary defect, nothing AI-specific | the code |

The class matters more than the fix. Choosing between `context` and `spec`
forces you to say whether the agent lacked information or you did — and those
have different remedies.

---

## Entries

Exercise A was built on 2 Nov 2026 (after the lab session, which I missed), with Claude Code
(Opus 5.5) doing the coding and me directing. Session log: `sessions/`.

### E1

- **Date**: 2026-11-02
- **What happened**: The first batch over 20 dev issues fired all calls back to back. The Gemini key is on the free tier (15 requests/minute), so 3 of 20 issues came back as `TriageFailure: LMRateLimitError`. The agent's retry is immediate, so the retry was also rate-limited and wasted.
- **Class**: `context`
- **Evidence**: `results/dev20.jsonl` (textual 5421, 5423, 5426); `src/triage/extract.py` retry loop
- **What I did about it**: Waited a minute and re-ran the 3 issues one by one (`results/dev20-retry.jsonl`). Recorded "retry has no backoff" in `docs/decisions.md`.
- **Did it work?**: Yes for the rerun; the code still has no backoff — the real fix (backoff on 429, separate from retry on invalid output) is open.

---

### E2

- **Date**: 2026-11-02
- **What happened**: The agent's first version of `load_issues` in `cli.py` iterated over `json.loads(...)` without narrowing its type, and `uv run pyright` (strict) failed with two "partially unknown" errors. It had also passed meaningless extra arguments to `Issue.model_validate`.
- **Class**: `bug`
- **Evidence**: pyright output: `cli.py:27:5 - error: Type of "rows" is partially unknown`
- **What I did about it**: Narrowed with `cast(list[object], ...)` and let Pydantic validate each row.
- **Did it work?**: Yes — `0 errors` (only the expected warnings in `extract.py`, the declared model boundary).

---

### E3

- **Date**: 2026-11-02
- **What happened**: The brief never defined severity, and the dataset has no gold severity. The agent invented a 4-level scale and a definition ("critical = outage, data loss or security hole") without asking. On 20 issues the model used only `low` and `medium` — never `high`/`critical` — so the field cannot drive escalation.
- **Class**: `spec`
- **Evidence**: `src/triage/extract.py` (`severity` OutputField desc); `results/dev20.jsonl`
- **What I did about it**: Wrote it down in `docs/decisions.md`. The fix belongs in the specification (see `issue-routing/spec.md` in the W2 examples, which defines severity → SLA), plus a hand-labelled gold set later in the course.
- **Did it work?**: Not yet — open.

---

### E4

- **Date**: 2026-11-02
- **What happened**: The model reports `confidence` 0.9–1.0 on every issue, including hono #3908 where it said `bug` and the gold label is `enhancement` (confidence 0.95). The agent had defined confidence as self-reported, so it carries almost no information.
- **Class**: `concept`
- **Evidence**: `results/dev20.jsonl`, hono 3908
- **What I did about it**: Documented in `review-findings.md` and `docs/decisions.md` that confidence is uncalibrated and unused.
- **Did it work?**: Open — calibration is W6/W7 material (ADR-0005 in the W2 examples says the same).

---

### E5

- **Date**: 2026-11-02
- **What happened**: When asked to prepare course notes, the agent first created a new folder `~/Documents/LLM-SE-2027`, although the workspace `CLAUDE.md` says course notes live under `~/Documents/Master/סמסטר-א-תשפז/`. After finding that, it listed the course folder with `head` truncation, missed the existing week folders, and created duplicates.
- **Class**: `context`
- **Evidence**: this session's log, early in the session
- **What I did about it**: Moved the file into `שבועות/W02 דרישות ו-SDLC/` and removed the duplicates.
- **Did it work?**: Yes.
