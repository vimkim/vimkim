#!/usr/bin/env python3
"""Refresh README project dates using an authenticated GitHub CLI."""

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


README_PATH = Path(__file__).resolve().parents[1] / "README.md"
PROJECT = re.compile(
    r"^(?P<link>- \[[^\]\n]+\]\(https://github\.com/"
    r"(?P<repo>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\))"
    r"(?: <sub>updated \d{4}-\d{2}-\d{2}</sub>)?"
    r"(?P<description>[^\n]*)$",
    re.MULTILINE,
)


def latest_commit_date(repo):
    try:
        result = subprocess.run(
            [
                "gh", "api", f"repos/{repo}/commits?per_page=1",
                "--jq", ".[0].commit.committer.date",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        timestamp = datetime.fromisoformat(result.stdout.strip().replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            raise ValueError("Missing timezone")
        return timestamp.astimezone(timezone.utc).date().isoformat()
    except (OSError, subprocess.SubprocessError, ValueError) as error:
        raise RuntimeError(
            f"Cannot read the latest commit for {repo}; check gh authentication, "
            "repository access, and whether the repository contains commits."
        ) from error


def refresh_dates(text, fetch_date=latest_commit_date):
    repos = dict.fromkeys(match["repo"] for match in PROJECT.finditer(text))
    if not repos:
        raise ValueError("No GitHub project entries found in README")

    # Fetch every date before changing the file, so failures preserve the README.
    dates = {repo: fetch_date(repo) for repo in repos}
    return PROJECT.sub(
        lambda match: (
            f'{match["link"]} <sub>updated {dates[match["repo"]]}</sub>'
            f'{match["description"]}'
        ),
        text,
    )


def main():
    original = README_PATH.read_text(encoding="utf-8")
    updated = refresh_dates(original)
    if updated != original:
        README_PATH.write_text(updated, encoding="utf-8")
        print("Updated project dates in README.md")
    else:
        print("Project dates are already current")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
