
"""Tests for TournamentLab team registration."""

import unittest

from tournament.teams import register_team, validate_team_name


class TestTeamRegistration(unittest.TestCase):

    def setUp(self):
        self.teams = []

    def test_register_first_team(self):
        team = register_team(self.teams, "Thunder")

        self.assertEqual(team["id"], "TM001")
        self.assertEqual(team["name"], "Thunder")
        self.assertEqual(len(self.teams), 1)

    def test_register_multiple_teams(self):
        first = register_team(self.teams, "Thunder")
        second = register_team(self.teams, "Comets")

        self.assertEqual(first["id"], "TM001")
        self.assertEqual(second["id"], "TM002")

    def test_team_name_is_trimmed(self):
        team = register_team(self.teams, "  Phoenix  ")

        self.assertEqual(team["name"], "Phoenix")

    def test_duplicate_name_is_rejected(self):
        register_team(self.teams, "Thunder")

        with self.assertRaises(ValueError):
            register_team(self.teams, " thunder ")

        self.assertEqual(len(self.teams), 1)

    def test_name_too_short_is_rejected(self):
        with self.assertRaises(ValueError):
            register_team(self.teams, "A")

    def test_name_too_long_is_rejected(self):
        with self.assertRaises(ValueError):
            register_team(self.teams, "A" * 31)

    def test_non_string_name_is_rejected(self):
        with self.assertRaises(ValueError):
            register_team(self.teams, 123)

    def test_validation_returns_cleaned_name(self):
        result = validate_team_name("  Rockets  ")

        self.assertEqual(result, "Rockets")


if __name__ == "__main__":
    unittest.main()