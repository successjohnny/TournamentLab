
"""Tests for TournamentLab JSON storage."""

import json
import tempfile
import unittest
from pathlib import Path

from tournament.fixtures import generate_fixtures, record_result
from tournament.storage import (
    load_tournament,
    save_tournament,
    validate_tournament_data,
)


class TestTournamentStorage(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Thunder"},
            {"id": "TM002", "name": "Comets"},
            {"id": "TM003", "name": "Phoenix"},
            {"id": "TM004", "name": "Rockets"},
        ]

        self.fixtures = generate_fixtures(self.teams)

    def test_save_and_load_tournament(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tournament.json"

            save_tournament(path, self.teams, self.fixtures)
            loaded_teams, loaded_fixtures = load_tournament(path)

            self.assertEqual(loaded_teams, self.teams)
            self.assertEqual(loaded_fixtures, self.fixtures)

    def test_saved_file_contains_schema_version(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tournament.json"

            save_tournament(path, self.teams, self.fixtures)

            with path.open(encoding="utf-8") as file:
                data = json.load(file)

            self.assertEqual(data["schema_version"], 1)

    def test_played_results_survive_save_and_load(self):
        record_result(self.fixtures[0], 2, 0)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tournament.json"

            save_tournament(path, self.teams, self.fixtures)
            _, loaded_fixtures = load_tournament(path)

            self.assertEqual(loaded_fixtures[0]["status"], "played")
            self.assertEqual(loaded_fixtures[0]["home_score"], 2)
            self.assertEqual(loaded_fixtures[0]["away_score"], 0)

    def test_invalid_schema_version_is_rejected(self):
        data = {
            "schema_version": 2,
            "teams": self.teams,
            "fixtures": self.fixtures,
        }

        with self.assertRaises(ValueError):
            validate_tournament_data(data)

    def test_boolean_schema_version_is_rejected(self):
        data = {
            "schema_version": True,
            "teams": self.teams,
            "fixtures": self.fixtures,
        }

        with self.assertRaises(ValueError):
            validate_tournament_data(data)

    def test_duplicate_team_ids_are_rejected(self):
        teams = [team.copy() for team in self.teams]
        teams[1]["id"] = teams[0]["id"]

        data = {
            "schema_version": 1,
            "teams": teams,
            "fixtures": self.fixtures,
        }

        with self.assertRaises(ValueError):
            validate_tournament_data(data)

    def test_duplicate_team_names_are_rejected(self):
        teams = [team.copy() for team in self.teams]
        teams[1]["name"] = " thunder "

        data = {
            "schema_version": 1,
            "teams": teams,
            "fixtures": self.fixtures,
        }

        with self.assertRaises(ValueError):
            validate_tournament_data(data)

    def test_unknown_team_reference_is_rejected(self):
        fixtures = [fixture.copy() for fixture in self.fixtures]
        fixtures[0]["home_team_id"] = "TM999"

        data = {
            "schema_version": 1,
            "teams": self.teams,
            "fixtures": fixtures,
        }

        with self.assertRaises(ValueError):
            validate_tournament_data(data)

    def test_duplicate_pairing_is_rejected(self):
        fixtures = [fixture.copy() for fixture in self.fixtures]
        fixtures[1]["home_team_id"] = fixtures[0]["home_team_id"]
        fixtures[1]["away_team_id"] = fixtures[0]["away_team_id"]

        data = {
            "schema_version": 1,
            "teams": self.teams,
            "fixtures": fixtures,
        }

        with self.assertRaises(ValueError):
            validate_tournament_data(data)

    def test_pending_fixture_with_score_is_rejected(self):
        fixtures = [fixture.copy() for fixture in self.fixtures]
        fixtures[0]["home_score"] = 2

        data = {
            "schema_version": 1,
            "teams": self.teams,
            "fixtures": fixtures,
        }

        with self.assertRaises(ValueError):
            validate_tournament_data(data)

    def test_played_fixture_with_boolean_score_is_rejected(self):
        fixtures = [fixture.copy() for fixture in self.fixtures]
        fixtures[0]["status"] = "played"
        fixtures[0]["home_score"] = True
        fixtures[0]["away_score"] = 0

        data = {
            "schema_version": 1,
            "teams": self.teams,
            "fixtures": fixtures,
        }

        with self.assertRaises(ValueError):
            validate_tournament_data(data)

    def test_played_fixture_with_negative_score_is_rejected(self):
        fixtures = [fixture.copy() for fixture in self.fixtures]
        fixtures[0]["status"] = "played"
        fixtures[0]["home_score"] = -1
        fixtures[0]["away_score"] = 0

        data = {
            "schema_version": 1,
            "teams": self.teams,
            "fixtures": fixtures,
        }

        with self.assertRaises(ValueError):
            validate_tournament_data(data)

    def test_invalid_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tournament.json"
            path.write_text("{invalid json", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_tournament(path)

    def test_missing_file_raises_file_not_found(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.json"

            with self.assertRaises(FileNotFoundError):
                load_tournament(path)


if __name__ == "__main__":
    unittest.main()