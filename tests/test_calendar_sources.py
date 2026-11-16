from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from oracle.calendar_fetch import ingest_calendar_from_text, resolve_calendar_events
from oracle.sources import build_sources, calendar_connected


class CalendarSources(unittest.TestCase):
    def test_ingest_calendar_from_json_array(self):
        blob = json.dumps(
            [
                {
                    "summary": "Hackathon demo screen record",
                    "start": "2026-11-11T19:00:00+01:00",
                    "end": "2026-11-11T19:45:00+01:00",
                }
            ]
        )
        events = ingest_calendar_from_text(f"calendar list\n{blob}")
        self.assertEqual(len(events), 1)
        self.assertIn("hackathon", events[0]["summary"].lower())

    def test_build_sources_git_this_repo(self):
        repo = "/home/ostheperson/dev/oracle-rubal"
        with patch("oracle.sources.calendar_connected", return_value=False):
            sources = build_sources(repo=repo, match="plugin")
        self.assertTrue(sources["git"]["ok"])
        self.assertFalse(sources["calendar"]["ok"])

    @patch("oracle.sources.resolve_calendar_events", return_value=([{"summary": "x", "start": "t"}], None))
    @patch("oracle.sources.calendar_connected", return_value=True)
    def test_build_sources_uses_fetched_events(self, _conn, _resolve):
        sources = build_sources(repo="/tmp/nope")
        self.assertTrue(sources["calendar"]["ok"])
        self.assertEqual(len(sources["calendar"]["events"]), 1)

    @patch("oracle.sources.load_cached_events", return_value=[])
    def test_calendar_connected_false_without_cache(self, _load):
        self.assertFalse(calendar_connected())

    @patch("oracle.sources.load_cached_events", return_value=[{"summary": "a", "start": "t"}])
    def test_calendar_connected_true_with_cache(self, _load):
        self.assertTrue(calendar_connected())

    @patch("oracle.calendar_fetch.load_cached_events", return_value=[{"summary": "cached", "start": "t"}])
    def test_resolve_calendar_events_cache_only(self, _load):
        events, err = resolve_calendar_events()
        self.assertEqual(len(events), 1)
        self.assertIsNone(err)

    def test_ingest_finds_json_after_noise(self):
        payload = json.dumps([{"summary": "Demo", "start": "2026-01-01T00:00:00Z", "end": ""}])
        events = ingest_calendar_from_text(f"stderr junk\n{payload}\nmore junk")
        self.assertEqual(len(events), 1)


if __name__ == "__main__":
    unittest.main()
