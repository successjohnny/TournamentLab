
"""Tests for TournamentLab fixture generation and results."""

import unittest

from tournament.fixtures import generate_fixtures, record_result


class TestFixtureGeneration(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Thunder"},
            {"id": "TM002", "name": "Comets"},
            {"id": "TM003", "name": "Phoenix"},
            {"id": "TM004", "name": "Rockets"},
        ]

    def test_four_teams_generate_six_fixtures(self):
        fixtures = generate_fixtures(self.teams)

        self.assertEqual(len(fixtures), 6)

    def test_fixture_ids_are_sequential(self):
        fixtures = generate_fixtures(self.teams)

        expected_ids = [f"M{i:03d}" for i in range(1, 7)]
        actual_ids = [fixture["id"] for fixture in fixtures]

        self.assertEqual(actual_ids, expected_ids)

    def test_every_fixture_is_initially_pending(self):
        fixtures = generate_fixtures(self.teams)

        for fixture in fixtures:
            self.assertEqual(fixture["status"], "pending")
            self.assertIsNone(fixture["home_score"])
            self.assertIsNone(fixture["away_score"])

    def test_no_team_plays_itself(self):
        fixtures = generate_fixtures(self.teams)

        for fixture in fixtures:
            self.assertNotEqual(
                fixture["home_team_id"],
                fixture["away_team_id"],
            )

    def test_duplicate_team_ids_are_rejected(self):
        invalid_teams = self.teams.copy()
        invalid_teams[1] = {
            "id": "TM001",
            "name": "Comets",
        }

        with self.assertRaises(ValueError):
            generate_fixtures(invalid_teams)

    def test_three_teams_are_rejected(self):
        with self.assertRaises(ValueError):
            generate_fixtures(self.teams[:3])

    def test_nine_teams_are_rejected(self):
        nine_teams = [
            {"id": f"TM{i:03d}", "name": f"Team {i}"}
            for i in range(1, 10)
        ]

        with self.assertRaises(ValueError):
            generate_fixtures(nine_teams)


class TestRecordResult(unittest.TestCase):

    def setUp(self):
        self.fixture = {
            "id": "M001",
            "home_team_id": "TM001",
            "away_team_id": "TM002",
            "status": "pending",
            "home_score": None,
            "away_score": None,
        }

    def test_valid_result_is_recorded(self):
        record_result(self.fixture, 3, 2)

        self.assertEqual(self.fixture["home_score"], 3)
        self.assertEqual(self.fixture["away_score"], 2)
        self.assertEqual(self.fixture["status"], "played")

    def test_zero_is_a_valid_score(self):
        record_result(self.fixture, 0, 0)

        self.assertEqual(self.fixture["home_score"], 0)
        self.assertEqual(self.fixture["away_score"], 0)

    def test_negative_home_score_is_rejected_without_mutation(self):
        original = self.fixture.copy()

        with self.assertRaises(ValueError):
            record_result(self.fixture, -1, 2)

        self.assertEqual(self.fixture, original)

    def test_negative_away_score_is_rejected_without_mutation(self):
        original = self.fixture.copy()

        with self.assertRaises(ValueError):
            record_result(self.fixture, 2, -1)

        self.assertEqual(self.fixture, original)

    def test_boolean_score_is_rejected(self):
        original = self.fixture.copy()

        with self.assertRaises(ValueError):
            record_result(self.fixture, True, 2)

        self.assertEqual(self.fixture, original)

    def test_decimal_score_is_rejected(self):
        original = self.fixture.copy()

        with self.assertRaises(ValueError):
            record_result(self.fixture, 2.5, 2)

        self.assertEqual(self.fixture, original)

    def test_played_fixture_cannot_receive_another_result(self):
        record_result(self.fixture, 2, 1)
        original = self.fixture.copy()

        with self.assertRaises(ValueError):
            record_result(self.fixture, 4, 0)

        self.assertEqual(self.fixture, original)


if __name__ == "__main__":
    unittest.main()