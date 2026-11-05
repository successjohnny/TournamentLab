
"""Tests for TournamentLab league standings."""

import unittest

from tournament.standings import (
    calculate_standings,
    get_champion,
    get_tournament_status,
)


class TestStandings(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Thunder"},
            {"id": "TM002", "name": "Comets"},
            {"id": "TM003", "name": "Phoenix"},
            {"id": "TM004", "name": "Rockets"},
        ]

        self.fixtures = [
            {
                "id": "M001",
                "home_team_id": "TM001",
                "away_team_id": "TM002",
                "status": "played",
                "home_score": 2,
                "away_score": 0,
            },
            {
                "id": "M002",
                "home_team_id": "TM001",
                "away_team_id": "TM003",
                "status": "played",
                "home_score": 1,
                "away_score": 1,
            },
            {
                "id": "M003",
                "home_team_id": "TM001",
                "away_team_id": "TM004",
                "status": "pending",
                "home_score": None,
                "away_score": None,
            },
            {
                "id": "M004",
                "home_team_id": "TM002",
                "away_team_id": "TM003",
                "status": "pending",
                "home_score": None,
                "away_score": None,
            },
            {
                "id": "M005",
                "home_team_id": "TM002",
                "away_team_id": "TM004",
                "status": "pending",
                "home_score": None,
                "away_score": None,
            },
            {
                "id": "M006",
                "home_team_id": "TM003",
                "away_team_id": "TM004",
                "status": "pending",
                "home_score": None,
                "away_score": None,
            },
        ]

    def test_only_played_fixtures_affect_standings(self):
        standings = calculate_standings(self.teams, self.fixtures)

        thunder = next(
            row for row in standings if row["team_id"] == "TM001"
        )

        self.assertEqual(thunder["P"], 2)

    def test_win_awards_three_points(self):
        standings = calculate_standings(self.teams, self.fixtures)

        thunder = next(
            row for row in standings if row["team_id"] == "TM001"
        )

        self.assertEqual(thunder["W"], 1)
        self.assertEqual(thunder["PTS"], 4)

    def test_draw_awards_one_point_each(self):
        standings = calculate_standings(self.teams, self.fixtures)

        thunder = next(
            row for row in standings if row["team_id"] == "TM001"
        )
        phoenix = next(
            row for row in standings if row["team_id"] == "TM003"
        )

        self.assertEqual(thunder["D"], 1)
        self.assertEqual(phoenix["D"], 1)

    def test_goal_difference_is_calculated(self):
        standings = calculate_standings(self.teams, self.fixtures)

        thunder = next(
            row for row in standings if row["team_id"] == "TM001"
        )

        self.assertEqual(thunder["GF"], 3)
        self.assertEqual(thunder["GA"], 1)
        self.assertEqual(thunder["GD"], 2)

    def test_standings_are_sorted_by_points(self):
        standings = calculate_standings(self.teams, self.fixtures)

        points = [row["PTS"] for row in standings]

        self.assertEqual(points, sorted(points, reverse=True))

    def test_pending_tournament_has_no_champion(self):
        champion = get_champion(self.teams, self.fixtures)

        self.assertIsNone(champion)

    def test_tournament_is_in_progress(self):
        status = get_tournament_status(self.fixtures)

        self.assertEqual(status, "in progress")

    def test_empty_fixture_list_is_not_completed(self):
        status = get_tournament_status([])

        self.assertEqual(status, "in progress")


if __name__ == "__main__":
    unittest.main()