# Project update dates

`project-dates.yml` refreshes the dates beside every GitHub repository bullet in
`README.md`, including private projects and the collapsed deprecated subsection.
New project links are picked up automatically; there is no separate project list.

The date is the UTC committer date of the latest commit on the repository's default
branch. Changes to issues, stars, or another branch do not affect it. The API
requests return only dates, and no private commit content is written to the profile.

The workflow runs daily at 03:17 KST, on relevant pushes to `main`, and through
`workflow_dispatch`. It commits only `README.md`, and only when dates change.
GitHub's scheduler can be delayed and disables schedules on public repositories
after 60 days without repository activity.

The existing `PAT` secret must allow reading commits in every listed repository.
For a fine-grained PAT, grant Contents: read for those repositories. The workflow's
`GITHUB_TOKEN` uses Contents: write to commit and push to this profile repository.
If a project cannot be read, the updater fails before writing any dates.

For a local refresh with an authenticated GitHub CLI:

```sh
python3 -B scripts/update_project_dates.py
python3 -B -m unittest discover -s scripts -p 'test_*.py'
```

References: [GitHub's commits API](https://docs.github.com/en/rest/commits/commits#list-commits),
[workflow schedules](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).
