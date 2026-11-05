
"""Tests for reproducible TournamentLab demo generation."""

import unittest

from tournament.demo import create_demo_tournament


class TestDemoTournament(unittest.TestCase):

    def test_demo_contains_four_teams_and_six_played_fixtures(self):
        teams, fixtures = create_demo_tournament(42)

        self.assertEqual(len(teams), 4)
        self.assertEqual(len(fixtures), 6)

        for fixture in fixtures:
            self.assertEqual(fixture["status"], "played")
            self.assertIs(type(fixture["home_score"]), int)
            self.assertIs(type(fixture["away_score"]), int)

    def test_same_seed_produces_same_results(self):
        teams_one, fixtures_one = create_demo_tournament(42)
        teams_two, fixtures_two = create_demo_tournament(42)

        self.assertEqual(teams_one, teams_two)
        self.assertEqual(fixtures_one, fixtures_two)

    def test_invalid_seed_is_rejected(self):
        with self.assertRaises(ValueError):
            create_demo_tournament(True)


if __name__ == "__main__":
    unittest.main()