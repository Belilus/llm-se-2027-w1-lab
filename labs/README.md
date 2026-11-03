# Labs — one folder per week

Code is shared across weeks and stays where the tooling expects it (`src/`, `tests/`,
`data/`, `tools/`). Each week's write-ups go in that week's folder here.

| Week | Folder | Lab | Status |
|---|---|---|---|
| W1 | [`W01/`](W01/) | Ship a triage feature (A), review an agent's diff (B) | A done; B open |
| W2 | [`W02/`](W02/) | Specifications: SRS, user stories, OpenSpec (`spec-lab/`) | set up, not started |

Starting a new week: `mkdir labs/WXX`, add a `README.md` with the brief and the list of
deliverables, and put every write-up for that lab in the folder. Code changes still go
in `src/` and `tests/`.

Files that stay at the repo root:

| File | Why it stays at the root |
|---|---|
| `improvement-log.md` | Runs all semester, one entry per agent mistake |
| `LAB.md`, `README.md` | Instructor's files; moving them breaks `git pull upstream main` |
| `sessions/` | `tools/export_session_log.py` writes there |
| `course-notes/` | Symlink to the Google Drive notes; gitignored, never pushed |
