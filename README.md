
# TournamentLab

A Python command-line esports league manager that registers teams, generates single round-robin fixtures, records match results, calculates league standings, and identifies the champion.

Built with Python's standard library, with automated tests using `unittest`.

## Features

- Register 4–8 teams.
- Validate team names and prevent case-insensitive duplicates.
- Assign stable team IDs.
- Generate single round-robin fixtures.
- Ensure every team plays every other team exactly once.
- Record non-negative integer match scores.
- Prevent duplicate result entry.
- Calculate league standings from completed fixtures.
- Rank teams by points, goal difference, goals scored, and team name.
- Save and load tournaments using validated JSON.
- Preserve saved data through atomic file replacement.
- Create a separate, reproducible demo using a random seed.
- Identify the champion only when all fixtures are completed.

## Technology

- Python 3.12+
- Python standard library
- JSON persistence
- `unittest` automated testing

No third-party packages or external esports APIs are required.

## Project structure

```text
TournamentLab/
├── main.py
├── tournament/
│   ├── __init__.py
│   ├── teams.py
│   ├── fixtures.py
│   ├── standings.py
│   ├── storage.py
│   ├── demo.py
│   └── cli.py
├── tests/
│   ├── __init__.py
│   ├── test_teams.py
│   ├── test_fixtures.py
│   ├── test_standings.py
│   ├── test_storage.py
│   ├── test_cli.py
│   └── test_demo.py
├── docs/
│   ├── design-decisions.md
│   └── ai-learning-log.md
├── .github/
│   └── workflows/
│       └── tests.yml
├── .gitignore
└── README.md
```

## Requirements

- Python 3.12 or later.
- Git (for cloning the repository).

## Run locally

Clone the repository:

```bash
git clone https://github.com/successjohnny/tournamentlab.git
cd tournamentlab
```

Start the application:

```bash
python3 main.py
```

The application presents an interactive menu.

## How to use

1. Register between four and eight teams.
2. Generate fixtures.
3. View the generated matches.
4. Record results using fixture IDs such as `M001`.
5. View the league standings.
6. Save the tournament.
7. Load a saved tournament when restarting the application.

### Demo simulation

Choose menu option `10` to create a separate simulated tournament.

Enter an integer seed, for example:

```text
42
```

The same seed produces the same simulated match results.

The demo is saved to `demo_tournament.json` and does not overwrite the main `tournament.json` file.

## Tournament rules

### Fixture generation

For N teams, the number of fixtures is:

```text
N × (N - 1) / 2
```

For four teams:

```text
4 × 3 / 2 = 6 fixtures
```

Each pair of teams plays exactly once.

### Points

| Match outcome | Points |
|---|---:|
| Win | 3 |
| Draw | 1 |
| Loss | 0 |

### Ranking

Teams are ranked by:

1. Points (highest first).
2. Goal difference (highest first).
3. Goals scored (highest first).
4. Team name (case-insensitive alphabetical order).

Goal difference:

```text
GD = GF - GA
```

Head-to-head ranking is not used.

### Champion

A champion is declared only when every fixture has been played.

Until then, the standings are marked as in progress.

## Data persistence

Tournament data is stored as JSON with a schema version.

The application validates team records, fixture references, unique pairings, fixture statuses, and scores before accepting saved data.

Invalid data is rejected rather than loaded into the active tournament.

## Run automated tests

```bash
python3 -m unittest discover -s tests -v
```

Check Python syntax:

```bash
python3 -m compileall -q .
```

## Design documentation

- [Design decisions](docs/design-decisions.md)
- [AI learning log](docs/ai-learning-log.md)

## Project status

The core CLI, tournament logic, JSON persistence, and seeded demo are implemented. Automated tests cover the main functionality.

## Author

**John Ikwuobe**

AI-Native Full-Stack Developer | Software Engineer

GitHub: [@successjohnny](https://github.com/successjohnny)