# llm-se-2027 W1 lab

Python 3.13, managed with uv.

```bash
uv sync                          # install
uv run pytest                    # tests
uv run pyright                   # type check
uv run python tools/verify_env.py
```

Source lives in `src/`. Tests in `tests/`. Both are shared by every week: W3, W5 and W6
keep evolving `src/triage/`, so code never moves into a week folder.

Each weekly lab's write-ups (findings, decisions, results, released diffs) live in
`labs/WXX/`; `labs/README.md` is the index. `improvement-log.md` stays at the root because
it runs all semester. `course-notes/` is a gitignored symlink to Asaf's notes in Google
Drive: read it for context, never commit it, never write code or secrets into it.
