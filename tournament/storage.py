
"""JSON persistence and validation for TournamentLab."""

import json
import os
import tempfile
from itertools import combinations
from pathlib import Path


SCHEMA_VERSION = 1
MIN_TEAMS = 4
MAX_TEAMS = 8


def validate_tournament_data(data: object) -> tuple[list[dict], list[dict]]:
    """Validate the complete tournament structure before accepting it."""

    if not isinstance(data, dict):
        raise ValueError("Tournament data must be a JSON object.")

    if set(data) != {"schema_version", "teams", "fixtures"}:
        raise ValueError("Tournament data has missing or unexpected fields.")

    if type(data["schema_version"]) is not int:
        raise ValueError("Schema version must be an integer.")

    if data["schema_version"] != SCHEMA_VERSION:
        raise ValueError("Unsupported tournament schema version.")

    teams = data["teams"]
    fixtures = data["fixtures"]

    if not isinstance(teams, list):
        raise ValueError("Teams must be a list.")

    if not MIN_TEAMS <= len(teams) <= MAX_TEAMS:
        raise ValueError("A tournament must have between 4 and 8 teams.")

    if not isinstance(fixtures, list):
        raise ValueError("Fixtures must be a list.")

    expected_fixture_count = len(teams) * (len(teams) - 1) // 2

    if len(fixtures) != expected_fixture_count:
        raise ValueError("Fixture count does not match the registered teams.")

    team_ids = set()
    normalized_names = set()

    for team in teams:
        if not isinstance(team, dict) or set(team) != {"id", "name"}:
            raise ValueError("Every team must contain only an ID and name.")

        team_id = team["id"]
        name = team["name"]

        if not isinstance(team_id, str) or not isinstance(name, str):
            raise ValueError("Team IDs and names must be text.")

        if not team_id.startswith("TM") or not team_id[2:].isdigit():
            raise ValueError("Invalid team ID format.")

        if len(team_id) != 5:
            raise ValueError("Invalid team ID format.")

        cleaned_name = name.strip()

        if not 2 <= len(cleaned_name) <= 30 or cleaned_name != name:
            raise ValueError("Team names must be trimmed and 2 to 30 characters.")

        if team_id in team_ids:
            raise ValueError("Duplicate team ID detected.")

        normalized_name = name.casefold()

        if normalized_name in normalized_names:
            raise ValueError("Duplicate team name detected.")

        team_ids.add(team_id)
        normalized_names.add(normalized_name)

    expected_pairs = {
        frozenset(pair)
        for pair in combinations(team_ids, 2)
    }

    actual_pairs = set()
    fixture_ids = set()

    for number, fixture in enumerate(fixtures, start=1):
        required_fields = {
            "id",
            "home_team_id",
            "away_team_id",
            "status",
            "home_score",
            "away_score",
        }

        if not isinstance(fixture, dict) or set(fixture) != required_fields:
            raise ValueError("Fixture contains missing or unexpected fields.")

        fixture_id = fixture["id"]

        if fixture_id != f"M{number:03d}":
            raise ValueError("Fixture IDs must be sequential.")

        if fixture_id in fixture_ids:
            raise ValueError("Duplicate fixture ID detected.")

        fixture_ids.add(fixture_id)

        home_id = fixture["home_team_id"]
        away_id = fixture["away_team_id"]

        if home_id not in team_ids or away_id not in team_ids:
            raise ValueError("Fixture references an unknown team.")

        if home_id == away_id:
            raise ValueError("A team cannot play against itself.")

        pair = frozenset((home_id, away_id))

        if pair in actual_pairs:
            raise ValueError("Duplicate team pairing detected.")

        actual_pairs.add(pair)

        status = fixture["status"]
        home_score = fixture["home_score"]
        away_score = fixture["away_score"]

        if status == "pending":
            if home_score is not None or away_score is not None:
                raise ValueError("Pending fixtures cannot have scores.")

        elif status == "played":
            if (
                type(home_score) is not int
                or home_score < 0
                or type(away_score) is not int
                or away_score < 0
            ):
                raise ValueError("Played fixtures require valid non-negative scores.")

        else:
            raise ValueError("Fixture status must be pending or played.")

    if actual_pairs != expected_pairs:
        raise ValueError("Fixtures do not cover every unique team pairing.")

    return teams, fixtures


def save_tournament(
    path: str | Path,
    teams: list[dict],
    fixtures: list[dict],
) -> None:
    """Validate and atomically save tournament data as JSON."""

    destination = Path(path)

    data = {
        "schema_version": SCHEMA_VERSION,
        "teams": teams,
        "fixtures": fixtures,
    }

    validate_tournament_data(data)

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=destination.parent,
            delete=False,
        ) as temporary_file:
            json.dump(data, temporary_file, indent=2, ensure_ascii=False)
            temporary_file.write("\n")
            temporary_path = temporary_file.name

        os.replace(temporary_path, destination)

    finally:
        if temporary_path is not None and os.path.exists(temporary_path):
            os.unlink(temporary_path)


def load_tournament(path: str | Path) -> tuple[list[dict], list[dict]]:
    """Load and validate tournament data from a JSON file."""

    source = Path(path)

    try:
        with source.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError("Tournament file contains invalid JSON.") from error

    teams, fixtures = validate_tournament_data(data)

    return teams, fixtures