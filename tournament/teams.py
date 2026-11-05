
"""Team registration and validation for TournamentLab."""

MIN_TEAM_NAME_LENGTH = 2
MAX_TEAM_NAME_LENGTH = 30


def validate_team_name(name: str) -> str:
    """Validate and return a cleaned team name."""
    if not isinstance(name, str):
        raise ValueError("Team name must be text.")

    cleaned_name = name.strip()

    if not MIN_TEAM_NAME_LENGTH <= len(cleaned_name) <= MAX_TEAM_NAME_LENGTH:
        raise ValueError("Team name must contain 2 to 30 characters.")

    return cleaned_name


def register_team(teams: list[dict], name: str) -> dict:
    """Register a team with a unique, stable ID."""
    cleaned_name = validate_team_name(name)
    normalized_name = cleaned_name.casefold()

    for team in teams:
        if team["name"].casefold() == normalized_name:
            raise ValueError("A team with that name already exists.")

    team_id = f"TM{len(teams) + 1:03d}"

    # Protect against accidental ID reuse if records were removed.
    existing_ids = {team["id"] for team in teams}
    while team_id in existing_ids:
        next_number = int(team_id[2:]) + 1
        team_id = f"TM{next_number:03d}"

    team = {
        "id": team_id,
        "name": cleaned_name,
    }

    teams.append(team)
    return team