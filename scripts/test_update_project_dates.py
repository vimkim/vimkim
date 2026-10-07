import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import update_project_dates as updater


class ProjectDateTests(unittest.TestCase):
    def test_refresh_preserves_content_and_is_idempotent(self):
        original = (
            "### Projects\n\n"
            "- [public](https://github.com/example/public) — Public project\n"
            "<details>\n<summary>Deprecated</summary>\n\n"
            "- [private](https://github.com/example/private) "
            "<sub>updated 2020-01-01</sub> — Private project (private)\n\n"
            "</details>\n\n"
            "- [Article](https://example.com/article)\n"
            "![asset](profile-3d-contrib/profile-night-green.svg)\n"
        )
        updated = updater.refresh_dates(original, lambda repo: "2026-10-07")
        without_dates = re.sub(r" <sub>updated [^<]+</sub>", "", updated)
        expected = original.replace(" <sub>updated 2020-01-01</sub>", "")
        self.assertEqual(without_dates, expected)
        self.assertEqual(updated.count("<sub>updated 2026-10-07</sub>"), 2)
        self.assertEqual(
            updater.refresh_dates(updated, lambda repo: "2026-10-07"), updated
        )

    def test_failed_repository_lookup_leaves_file_untouched(self):
        original = (
            "- [public](https://github.com/example/public) — Public\n"
            "- [private](https://github.com/example/private) — Private\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            readme.write_text(original, encoding="utf-8")
            with patch.object(updater, "README_PATH", readme), patch.object(
                updater.subprocess, "run",
                side_effect=[
                    subprocess.CompletedProcess([], 0, "2026-10-07T00:00:00Z\n"),
                    subprocess.CalledProcessError(1, "gh"),
                ],
            ):
                with self.assertRaisesRegex(RuntimeError, "example/private"):
                    updater.main()
            self.assertEqual(readme.read_text(encoding="utf-8"), original)

    def test_dates_use_utc_and_reject_missing_commits(self):
        with patch.object(updater.subprocess, "run") as request:
            request.return_value.stdout = "2026-10-07T01:00:00+09:00\n"
            self.assertEqual(updater.latest_commit_date("example/repo"), "2026-10-06")
            request.return_value.stdout = "null\n"
            with self.assertRaises(RuntimeError):
                updater.latest_commit_date("example/repo")


if __name__ == "__main__":
    unittest.main()
