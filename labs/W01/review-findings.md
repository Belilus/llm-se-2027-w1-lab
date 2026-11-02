Name: Asaf Belilus
Date: 2026-11-02

# Exercise A - Execution findings

Ran `src/triage/` (model `gemini/gemini-3.5-flash-lite`, temperature 0) on 20 dev issues:
7 hono, 7 litestar, 6 textual. Outputs: `results/dev20.jsonl`, reruns in `results/dev20-retry.jsonl`.

---
### Surprise 1

- **Input issue json**: textual #5421, #5423, #5426 (dev.json)
- **Output triaged issue**: `TriageFailure`, reason `model call failed: LMRateLimitError` (HTTP 429, free tier: 15 requests/minute)
- **What is surprising**: 3/20 failed for a reason that has nothing to do with the issue. The failure path worked (the batch continued, the raw error was kept), but the retry fired immediately and was rate-limited too. "Retry on invalid output" and "back off on rate limit" are different policies; I had only one. Rerun a minute later: all 3 succeeded.

### Surprise 2

- **Input issue json**: hono #3908 "`Content-Type` header only works with `ctx.body()`" (gold_type: enhancement)
- **Output triaged issue**: `issue_type: bug`, `confidence: 0.95`
- **What is surprising**: Wrong (vs. gold) and 95% confident. Across all 20 issues confidence was between 0.9 and 1.0. Self-reported confidence does not separate right from wrong answers, so a threshold like "escalate below 0.6" would never fire.

### Surprise 3

- **Input issue json**: all 20
- **Output triaged issue**: severity was `low` 8 times and `medium` 12 times; never `high` or `critical`
- **What is surprising**: The field meant to drive escalation has collapsed to two values. There is no gold severity, so I cannot say whether that is wrong — only that nothing measures it.

### Surprise 4

- **Input issue json**: hono #3891, #3926, #3935, #3962, #3976; all 6 textual issues
- **Output triaged issue**: gold_type is null for 11 of the 20
- **What is surprising**: For more than half of the sample there is no label to compare to, so "accuracy" on 20 issues is really accuracy on 9. On those 9, issue_type matched gold 8 times.

### Surprise 5

- **Input issue json**: hono #3935 "ci: type error due to Deno version increase…"
- **Output triaged issue**: `issue_type: bug`, `component: ci`
- **What is surprising**: CI/maintenance work is labelled a bug, because my enum has no place for it (`meta` exists only for hono announcements). Free-text components drift too: `widgets`, `datatable`, `markdown` for textual; `ci`, `bun`, `types` for hono — none of them in the per-repo taxonomy in `config/repos.toml`.


# Exercise B — Review findings

## Part 1 — found by reading

Record every problem you find in the released diff. One block per finding.
Add as many as you need. Do not delete the unused ones — an empty block is
information too.

**These lock at 1:13.** Once you start running the code, anything new goes in
part 2 instead. That boundary is the measurement: without it there is no way to
tell what reading caught from what the test runner caught.

Confidence: `certain` | `probable` | `uncertain`

---

### Finding 1

- **Location** (file:line):
- **Confidence**:
- **What is wrong**:
- **Why it matters** (what breaks, for whom, when):
- **What would have caught this** (a test? a type? a review rule? nothing?):

---

### Finding 2

- **Location**:
- **Confidence**:
- **What is wrong**:
- **Why it matters**:
- **What would have caught this**:

---

### Finding 3

- **Location**:
- **Confidence**:
- **What is wrong**:
- **Why it matters**:
- **What would have caught this**:

---

### Finding 4

- **Location**:
- **Confidence**:
- **What is wrong**:
- **Why it matters**:
- **What would have caught this**:

---

### Finding 5

- **Location**:
- **Confidence**:
- **What is wrong**:
- **Why it matters**:
- **What would have caught this**:

---

### Finding 6

- **Location**:
- **Confidence**:
- **What is wrong**:
- **Why it matters**:
- **What would have caught this**:

---

## Part 2 — found by running

After `git apply`, `uv run pytest`, `uv run pyright` and the batch run.

### What the tooling found that I did not

- **Which tool** (pytest / pyright / running it):
- **What it showed**:
- **Would I have found this by reading?** (be honest):

### What I found by reading that the tooling did not

- 

### Anything the tooling reported that turned out not to be a problem

- 

---

## Scoring (fill in after the reveal)

| | part 1 (reading) | part 1 + part 2 |
|---|---|---|
| Seeded defects found | | |
| Seeded defects missed | | |
| False positives | | |

**Reading detection rate**: found / (found + missed) = ____%

**Combined detection rate**: found / (found + missed) = ____%

The gap between those two is not a measure of you. It is a measure of which
defects a machine can catch and which ones still need a person — and the
second group is the reason this course exists.

### One sentence: what did you miss, and why do you think you missed it?


