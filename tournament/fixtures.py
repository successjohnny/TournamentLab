
"""Round-robin fixture generation and result recording."""

from itertools import combinations


MIN_TEAMS = 4
MAX_TEAMS = 8


def generate_fixtures(teams: list[dict]) -> list[dict]:
    """Generate one fixture for every unique pair of teams."""

    if not MIN_TEAMS <= len(teams) <= MAX_TEAMS:
        raise ValueError("A tournament must have between 4 and 8 teams.")

    team_ids = [team["id"] for team in teams]

    if len(team_ids) != len(set(team_ids)):
        raise ValueError("Team IDs must be unique.")

    fixtures = []

    for number, (home_team, away_team) in enumerate(
        combinations(teams, 2), start=1
    ):
        fixture = {
            "id": f"M{number:03d}",
            "home_team_id": home_team["id"],
            "away_team_id": away_team["id"],
            "status": "pending",
            "home_score": None,
            "away_score": None,
        }

        fixtures.append(fixture)

    return fixtures


def record_result(
    fixture: dict,
    home_score: int,
    away_score: int,
) -> dict:
    """Validate and record a result on a pending fixture."""

    if type(home_score) is not int or home_score < 0:
        raise ValueError("Home score must be a non-negative integer.")

    if type(away_score) is not int or away_score < 0:
        raise ValueError("Away score must be a non-negative integer.")

    if fixture["status"] != "pending":
        raise ValueError("This fixture has already been played.")

    fixture["home_score"] = home_score
    fixture["away_score"] = away_score
    fixture["status"] = "played"

    return fixture