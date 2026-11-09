"""Outages must not turn cached data into a supposedly fresh snapshot."""

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

import update_profile


class ProfileRefreshTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.assets = Path(self.directory.name)
        self.cached = {"updated": "2025-01-01", "repositories": []}
        self.snapshot = self.assets / "profile-data.json"
        self.snapshot.write_text(json.dumps(self.cached))
        self.patch = patch.object(update_profile, "ASSETS", self.assets)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def error(self, code):
        return HTTPError("https://github.com/example", code, "Unavailable", {}, None)

    def test_outage_fallback_keeps_date_and_warns(self):
        original = self.snapshot.read_bytes()
        output = io.StringIO()
        with patch.object(update_profile, "collect", side_effect=self.error(504)), redirect_stdout(output):
            data, fresh = update_profile.load_profile_data(allow_cached=True)
        self.assertFalse(fresh)
        self.assertEqual(data, self.cached)
        self.assertEqual(self.snapshot.read_bytes(), original)
        self.assertIn("::warning", output.getvalue())
        self.assertIn("2025-01-01", output.getvalue())
        self.assertIn("has not been refreshed", output.getvalue())

    def test_default_fetch_remains_strict(self):
        with patch.object(update_profile, "collect", side_effect=self.error(504)):
            with self.assertRaises(HTTPError):
                update_profile.load_profile_data()

    def test_authentication_failures_do_not_use_cache(self):
        with patch.object(update_profile, "collect", side_effect=self.error(403)):
            with self.assertRaises(HTTPError):
                update_profile.load_profile_data(allow_cached=True)

    def test_successful_fetch_is_identified_as_fresh(self):
        new = {"updated": "2025-01-02", "repositories": []}
        with patch.object(update_profile, "collect", return_value=new):
            data, fresh = update_profile.load_profile_data(allow_cached=True)
        self.assertTrue(fresh)
        self.assertEqual(data, new)


if __name__ == "__main__":
    unittest.main()
