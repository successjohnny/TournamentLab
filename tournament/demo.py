
"""Reproducible demo tournament generation."""

import random

from tournament.fixtures import generate_fixtures, record_result
from tournament.teams import register_team


DEMO_TEAM_NAMES = ["Thunder", "Comets", "Phoenix", "Rockets"]


def create_demo_tournament(seed: int) -> tuple[list[dict], list[dict]]:
    """Create a separate tournament with reproducible simulated results."""

    if type(seed) is not int:
        raise ValueError("The demo seed must be an integer.")

    rng = random.Random(seed)

    teams: list[dict] = []

    for name in DEMO_TEAM_NAMES:
        register_team(teams, name)

    fixtures = generate_fixtures(teams)

    for fixture in fixtures:
        home_score = rng.randint(0, 5)
        away_score = rng.randint(0, 5)

        record_result(fixture, home_score, away_score)

    return teams, fixtures