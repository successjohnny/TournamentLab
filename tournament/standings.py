
"""League standings calculations for TournamentLab."""


def calculate_standings(
    teams: list[dict],
    fixtures: list[dict],
) -> list[dict]:
    """Calculate and rank teams using completed fixtures only."""

    standings = {}

    # Create a starting record for every registered team.
    for team in teams:
        team_id = team["id"]

        standings[team_id] = {
            "team_id": team_id,
            "name": team["name"],
            "P": 0,
            "W": 0,
            "D": 0,
            "L": 0,
            "GF": 0,
            "GA": 0,
            "GD": 0,
            "PTS": 0,
        }

    # Process completed fixtures only.
    for fixture in fixtures:
        if fixture["status"] != "played":
            continue

        home_id = fixture["home_team_id"]
        away_id = fixture["away_team_id"]
        home_score = fixture["home_score"]
        away_score = fixture["away_score"]

        home = standings[home_id]
        away = standings[away_id]

        home["P"] += 1
        away["P"] += 1

        home["GF"] += home_score
        home["GA"] += away_score

        away["GF"] += away_score
        away["GA"] += home_score

        if home_score > away_score:
            home["W"] += 1
            home["PTS"] += 3
            away["L"] += 1

        elif home_score < away_score:
            away["W"] += 1
            away["PTS"] += 3
            home["L"] += 1

        else:
            home["D"] += 1
            away["D"] += 1
            home["PTS"] += 1
            away["PTS"] += 1

    # Calculate goal difference for every team.
    for row in standings.values():
        row["GD"] = row["GF"] - row["GA"]

    # Apply the tournament's ranking rules.
    return sorted(
        standings.values(),
        key=lambda row: (
            -row["PTS"],
            -row["GD"],
            -row["GF"],
            row["name"].casefold(),
        ),
    )


def get_tournament_status(fixtures: list[dict]) -> str:
    """Return whether the tournament is in progress or completed."""

    if fixtures and all(
        fixture["status"] == "played" for fixture in fixtures
    ):
        return "completed"

    return "in progress"


def get_champion(
    teams: list[dict],
    fixtures: list[dict],
) -> dict | None:
    """Return the champion only after every fixture is played."""

    if get_tournament_status(fixtures) != "completed":
        return None

    standings = calculate_standings(teams, fixtures)

    return standings[0] if standings else None