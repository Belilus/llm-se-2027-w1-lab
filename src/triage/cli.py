"""Command line: triage one issue (or the first N of a split) and print JSON records.

    uv run python -m triage.cli --split dev --number 3891 --repo hono
    uv run python -m triage.cli --split dev --limit 20
    uv run python -m triage.cli --file my_issue.json

The sealed test split is refused on purpose.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

from dotenv import load_dotenv

from triage.extract import dspy_predictor, model_name, triage
from triage.schema import Issue

SNAPSHOT = Path(__file__).resolve().parents[2] / "data" / "snapshot"


def load_issues(path: Path) -> list[Issue]:
    data: object = json.loads(path.read_text(encoding="utf-8"))
    rows: list[object] = list(cast(list[object], data)) if isinstance(data, list) else [data]
    # Unknown keys (labels, comments, gold_*) are dropped by the model, on purpose.
    return [Issue.model_validate(row) for row in rows]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="triage", description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--split", choices=["train", "dev"], help="snapshot split to read")
    source.add_argument("--file", type=Path, help="a JSON file holding one issue or a list")
    parser.add_argument("--repo", help="only issues from this repo")
    parser.add_argument("--number", type=int, help="only this issue number")
    parser.add_argument("--limit", type=int, default=1, help="how many issues to triage (default 1)")
    args = parser.parse_args(argv)

    load_dotenv()
    path: Path = args.file if args.file else SNAPSHOT / f"{args.split}.json"
    issues = load_issues(path)
    if args.repo:
        issues = [i for i in issues if i.repo == args.repo]
    if args.number is not None:
        issues = [i for i in issues if i.number == args.number]
    if not issues:
        print("no matching issue", file=sys.stderr)
        return 1

    predictor = dspy_predictor()
    model = model_name()
    failures = 0
    for issue in issues[: args.limit]:
        result = triage(issue, predictor, model)
        failures += result.__class__.__name__ == "TriageFailure"
        print(result.model_dump_json())
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
