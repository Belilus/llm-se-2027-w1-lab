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

After `git apply`, `uv run pytest`, `uv run pyright` and the batch run (3.11.2026).

**How this part was done.** I missed the lab session and left part 1 empty when I locked
it: I did not know yet what to look for in a diff. Part 2 was done with Claude Code: it
ran the tools, then walked me through the diff line by line, and I wrote this section
with it. So the "found by reading" list below was found by an AI reading the diff, not by
me. That is the honest version of the measurement.

### What the tooling found that I did not

- **Which tool**: pytest
- **What it showed**: 15 passed. The tests are green, as the agent claimed. That is the
  finding: green tests here prove nothing about the batch path (see below).
- **Would I have found this by reading?** Not applicable; it is not a defect.

- **Which tool**: running it (`batch --split dev --offline`)
- **What it showed**: crash, `ModuleNotFoundError: No module named 'levenshtein_fast'`,
  in `router.py` `find_duplicates` → `similarity.py:7`. The main command the change adds
  does not run. No test reaches that import: every batch test has 0 or 1 issues, and
  `find_duplicates` returns early when `len(issues) < 2`.
- **Would I have found this by reading?** Yes. The package is not in `pyproject.toml`,
  and the `# type: ignore[import-not-found]` on that line says so out loud.

- **Which tool**: pyright
- **What it showed**: 1 error, `similarity.py:11` "Argument type is unknown" (the result
  of `ratio` from the unresolved import).
- **Would I have found this by reading?** Yes, same root cause as the crash.

### What was found by reading that the tooling did not

1. **The batch path bypasses validation** (`extract.py` `triage_raw`, `router.py`
   `route_raw`). Raw model strings go straight to routing, skipping `TriageRecord` and the
   `coerce_*` functions. Checked by calling `route_raw` directly: severity `"Critical"`
   gives `sla_hours=72, escalate=False` (the correct answer is 4 and True); `"High"` gives
   72 instead of 24; `"urgent"` gives 72 with no error; issue type `"Bug"` lands in
   `triage-clarify`. The justification ("so batches stay fast") does not hold: the model
   call dominates, not building a record.
2. **Silent default contradicts the policy** (`policy.py` `DEFAULT_SLA_HOURS`,
   `sla_for_raw`). The docstring of `sla_for` says the `KeyError` is deliberate, so a bad
   severity fails loudly instead of getting "a plausible-looking default that nobody ever
   notices". The change adds exactly that default.
3. **Two routers disagree on the same issue** (`router.py`). `route_raw` drops both
   rules in `route`: bug without repro → `triage-clarify`, and high severity with low
   confidence → escalate. A high-severity bug, no repro, confidence 0.3: `route` sends it
   to `triage-clarify`, `route_raw` to `engineering`.
4. **The stub hides it** (`stub.py` `triage_raw`). The stub builds a validated record
   and then flattens it, so `--offline` always produces clean values. Only the live path
   is broken, and no test runs the live path.
5. **Shell injection** (`similarity.py` `blame_context`). Builds a shell command from the
   issue title with an f-string and runs it with `shell=True`. Issue titles are untrusted
   public text; a title with a `'` in it runs arbitrary commands. The function is not
   called anywhere (dead code), and `extract.py` says issue text must "never [go] near a
   shell".
6. **Unknown dependency** (`similarity.py:7`). `levenshtein_fast` is not declared, and
   its warning is silenced. An agent-invented package name is a supply-chain risk
   (someone can register it). We did not install it.
7. **Quadratic duplicate detection** (`router.py` `find_duplicates`). The double loop
   visits all n² pairs and skips half; 240 issues is ~57k iterations, a 10k-issue day is
   10^8. Dedup by `number` alone ignores `repo`, so issue #12 in two repos collapses into one.
8. **Vocabulary break** (`router.py`, `policy.py`: `ticket_priority`). `schema.py` says
   nothing in the package calls severity "priority". Small, but it shows the agent did not
   read the codebase's rules.
9. **Tests that confirm the wrong thing** (`tests/exercise_b/test_batch.py`). Fixtures
   use strings `"true"` and `"0.9"`, which locks in the unvalidated shape as normal. No
   test has two or more issues, so duplicate detection is never exercised. `Routing` has
   no issue number, so a report cannot say which issue went where.

### Anything the tooling reported that turned out not to be a problem

- The pyright warnings in `extract.py` (`reportUnknownMemberType` on dspy) were there
  before the change; they are not caused by it.

### What would have had to be different for these to be caught

- A test with two or more issues, and one that feeds `route_raw` a capitalised severity,
  would have caught the crash and finding 1.
- One routing function that only accepts a `TriageRecord` makes findings 1–4 impossible
  by type: pyright would reject passing a raw dict.
- A review rule: any new dependency, `subprocess` or `shell=True` needs explicit sign-off
  (findings 5, 6).
- Reading the docstrings of the files the diff touches: they state the rules that
  findings 2, 5 and 8 break.

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


