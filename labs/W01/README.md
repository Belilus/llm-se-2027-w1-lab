# W1 lab — Ship it, then review it

Instructions: [`LAB.md`](../../LAB.md) at the repo root (instructor's file).
Notes and the slide summary: `course-notes/שבועות/W01 קוד זול, אמון יקר/`.

| File | What | Status |
|---|---|---|
| `decisions.md` | Decisions the brief did not specify | done (Exercise A) |
| `review-findings.md` | Exercise A surprises; Exercise B parts 1 and 2; scoring | A done; B empty |
| `results/` | Exercise A run over 20 dev issues | done |
| `exercise-b/` | Released diff and its README | to review |
| `../../src/triage/` | Exercise A code | done |
| `../../src/triage_by_agent/` | The other implementation, before the agent's change | released |

## Exercise B with the new paths

The diff's own paths are relative to the repo root, so run these from the root.

Part 1 (reading, no AI, no running):

```bash
code labs/W01/exercise-b/agent-change.diff
```

Part 2 (after part 1 is locked):

```bash
git apply labs/W01/exercise-b/agent-change.diff
uv run pytest
uv run pyright
uv run python -m triage_by_agent.cli batch --split dev --offline
```

Undo: `git checkout -- src/triage_by_agent` and `rm -r tests/exercise_b`.
