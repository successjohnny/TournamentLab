
"""Interactive command-line interface for TournamentLab."""

from pathlib import Path

from tournament.demo import create_demo_tournament
from tournament.fixtures import generate_fixtures, record_result
from tournament.standings import (
    calculate_standings,
    get_champion,
    get_tournament_status,
)
from tournament.storage import load_tournament, save_tournament
from tournament.teams import register_team


DEFAULT_DATA_FILE = Path("tournament.json")


def display_menu(output_fn=print) -> None:
    """Display the main application menu."""

    output_fn("\n========== TOURNAMENTLAB ==========")
    output_fn("1. Register a team")
    output_fn("2. View registered teams")
    output_fn("3. Generate fixtures")
    output_fn("4. View fixtures")
    output_fn("5. Record a match result")
    output_fn("6. View league standings")
    output_fn("7. Save tournament")
    output_fn("8. Load tournament")
    output_fn("9. Exit")
    output_fn("10. Create a separate seeded demo")
    output_fn("===================================")


def display_teams(teams: list[dict], output_fn=print) -> None:
    """Display all registered teams."""

    if not teams:
        output_fn("No teams have been registered yet.")
        return

    output_fn("\nREGISTERED TEAMS")

    for team in teams:
        output_fn(f'{team["id"]} - {team["name"]}')

    output_fn(f"Total teams: {len(teams)}")


def display_fixtures(
    fixtures: list[dict],
    teams: list[dict],
    output_fn=print,
) -> None:
    """Display fixtures with team names and result status."""

    if not fixtures:
        output_fn("No fixtures have been generated yet.")
        return

    team_names = {
        team["id"]: team["name"]
        for team in teams
    }

    output_fn("\nFIXTURES")

    for fixture in fixtures:
        home_name = team_names[fixture["home_team_id"]]
        away_name = team_names[fixture["away_team_id"]]

        if fixture["status"] == "played":
            result = (
                f'{fixture["home_score"]} - {fixture["away_score"]}'
            )
        else:
            result = "Pending"

        output_fn(
            f'{fixture["id"]}: {home_name} vs {away_name} | {result}'
        )


def display_standings(
    teams: list[dict],
    fixtures: list[dict],
    output_fn=print,
) -> None:
    """Display the current league table and tournament status."""

    if not fixtures:
        output_fn("Generate fixtures before viewing the league table.")
        return

    standings = calculate_standings(teams, fixtures)

    output_fn("\nLEAGUE STANDINGS")
    output_fn("-" * 75)
    output_fn(
        f'{"TEAM":<12} {"P":>3} {"W":>3} {"D":>3} '
        f'{"L":>3} {"GF":>3} {"GA":>3} {"GD":>4} {"PTS":>4}'
    )
    output_fn("-" * 75)

    for row in standings:
        output_fn(
            f'{row["name"]:<12} '
            f'{row["P"]:>3} {row["W"]:>3} {row["D"]:>3} '
            f'{row["L"]:>3} {row["GF"]:>3} {row["GA"]:>3} '
            f'{row["GD"]:>4} {row["PTS"]:>4}'
        )

    status = get_tournament_status(fixtures)
    output_fn("-" * 75)
    output_fn(f"Tournament status: {status.title()}")

    champion = get_champion(teams, fixtures)

    if champion is not None:
        output_fn(f'CHAMPION: {champion["name"]}')
    else:
        output_fn("Champion: Not yet decided.")


def _save(
    data_file: Path,
    teams: list[dict],
    fixtures: list[dict],
    output_fn,
) -> bool:
    """Save a generated tournament and report the outcome."""

    if not fixtures:
        output_fn("Generate fixtures before saving the tournament.")
        return False

    try:
        save_tournament(data_file, teams, fixtures)
    except (OSError, ValueError) as error:
        output_fn(f"Could not save tournament: {error}")
        return False

    output_fn(f"Tournament saved to {data_file}.")
    return True


def _register_team(
    teams: list[dict],
    fixtures: list[dict],
    input_fn,
    output_fn,
) -> None:
    """Collect and register one team."""

    if fixtures:
        output_fn(
            "Teams cannot be changed after fixtures have been generated."
        )
        return

    if len(teams) >= 8:
        output_fn("The tournament already has the maximum of 8 teams.")
        return

    name = input_fn("Enter team name: ")

    try:
        team = register_team(teams, name)
    except ValueError as error:
        output_fn(f"Registration failed: {error}")
        return

    output_fn(f'Team registered: {team["id"]} - {team["name"]}')

    if len(teams) < 4:
        output_fn(f"{4 - len(teams)} more team(s) needed to generate fixtures.")


def _generate(
    teams: list[dict],
    fixtures: list[dict],
    data_file: Path,
    output_fn,
) -> list[dict]:
    """Generate fixtures once at least four teams are registered."""

    if fixtures:
        output_fn("Fixtures have already been generated.")
        return fixtures

    try:
        new_fixtures = generate_fixtures(teams)
    except ValueError as error:
        output_fn(f"Could not generate fixtures: {error}")
        return fixtures

    output_fn(f"Generated {len(new_fixtures)} fixtures.")
    _save(data_file, teams, new_fixtures, output_fn)

    return new_fixtures


def _record_match_result(
    teams: list[dict],
    fixtures: list[dict],
    data_file: Path,
    input_fn,
    output_fn,
) -> None:
    """Collect, validate, record, and save a match result."""

    if not fixtures:
        output_fn("Generate fixtures before recording results.")
        return

    fixture_id = input_fn("Enter fixture ID (e.g. M001): ").strip().upper()

    fixture = next(
        (item for item in fixtures if item["id"] == fixture_id),
        None,
    )

    if fixture is None:
        output_fn("Fixture not found.")
        return

    try:
        home_score = int(input_fn("Enter home team score: "))
        away_score = int(input_fn("Enter away team score: "))
        record_result(fixture, home_score, away_score)

    except ValueError as error:
        output_fn(f"Result not recorded: {error}")
        return

    output_fn("Match result recorded successfully.")
    _save(data_file, teams, fixtures, output_fn)


def _load(
    data_file: Path,
    output_fn,
) -> tuple[list[dict], list[dict]] | None:
    """Load a tournament only after successful validation."""

    try:
        teams, fixtures = load_tournament(data_file)
    except (OSError, ValueError) as error:
        output_fn(f"Could not load tournament: {error}")
        return None

    output_fn(f"Tournament loaded from {data_file}.")
    return teams, fixtures


def _create_demo(
    data_file: Path,
    input_fn,
    output_fn,
) -> None:
    """Create and save a separate, reproducible demo tournament."""

    demo_file = data_file.with_name("demo_tournament.json")

    if demo_file.exists():
        confirmation = input_fn(
            "A demo file already exists. Overwrite it? Type YES to confirm: "
        ).strip()

        if confirmation != "YES":
            output_fn("Demo creation cancelled. Existing file was preserved.")
            return

    seed_text = input_fn("Enter an integer random seed: ").strip()

    try:
        seed = int(seed_text)
        teams, fixtures = create_demo_tournament(seed)
        save_tournament(demo_file, teams, fixtures)

    except (ValueError, OSError) as error:
        output_fn(f"Could not create demo tournament: {error}")
        return

    output_fn(f"Demo tournament created using seed {seed}.")
    output_fn(f"Demo saved separately to {demo_file}.")
    display_standings(teams, fixtures, output_fn)


def run_cli(
    data_file: str | Path = DEFAULT_DATA_FILE,
    input_fn=input,
    output_fn=print,
) -> None:
    """Run the TournamentLab interactive application."""

    data_file = Path(data_file)
    teams: list[dict] = []
    fixtures: list[dict] = []

    output_fn("Welcome to TournamentLab!")

    while True:
        display_menu(output_fn)
        choice = input_fn("Choose an option (1-10): ").strip()

        if choice == "1":
            _register_team(teams, fixtures, input_fn, output_fn)

        elif choice == "2":
            display_teams(teams, output_fn)

        elif choice == "3":
            fixtures = _generate(
                teams, fixtures, data_file, output_fn
            )

        elif choice == "4":
            display_fixtures(fixtures, teams, output_fn)

        elif choice == "5":
            _record_match_result(
                teams, fixtures, data_file, input_fn, output_fn
            )

        elif choice == "6":
            display_standings(teams, fixtures, output_fn)

        elif choice == "7":
            _save(data_file, teams, fixtures, output_fn)

        elif choice == "8":
            loaded = _load(data_file, output_fn)

            if loaded is not None:
                teams, fixtures = loaded

        elif choice == "9":
            output_fn("Thank you for using TournamentLab. Goodbye!")
            break

        elif choice == "10":
            _create_demo(data_file, input_fn, output_fn)

        else:
            output_fn("Invalid choice. Please enter a number from 1 to 10.")