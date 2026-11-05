
# TournamentLab — Design Decisions

## 1. Python standard library

The project uses Python's standard library to avoid unnecessary dependencies and demonstrate core Python programming skills.

## 2. Modular architecture

The application separates responsibilities into modules:

- `teams.py`: team registration and name validation.
- `fixtures.py`: fixture generation and result recording.
- `standings.py`: league calculations and champion selection.
- `storage.py`: JSON persistence and data validation.
- `demo.py`: reproducible demo tournament generation.
- `cli.py`: interactive user interface.
- `main.py`: application entry point.

This separation makes the application easier to test, maintain, and extend.

## 3. Stable team identifiers

Each team receives a unique ID such as `TM001`.

Team IDs are used in fixtures instead of relying on team names. This separates identity from display labels.

## 4. Single round-robin scheduling

The application uses pair combinations to generate every unique team pairing exactly once.

For N teams:

`N × (N - 1) / 2`

This prevents duplicate fixtures and guarantees the expected fixture count.

## 5. Result validation

Scores must be non-negative integers.

Boolean values are explicitly rejected because Python treats `bool` as a subclass of `int`.

A fixture must still be pending before a result can be recorded.

Validation occurs before mutation to prevent partially recorded results.

## 6. Derived standings

Standings are calculated from completed fixtures instead of being stored separately.

This avoids inconsistent points, goal differences, and match statistics when results change.

## 7. Ranking rules

The ranking order is:

1. Points.
2. Goal difference.
3. Goals scored.
4. Case-insensitive team name.

Head-to-head rules are intentionally excluded to keep ranking predictable.

## 8. JSON persistence

JSON was selected because it is readable, portable, and supported by Python's standard library.

The saved data includes `schema_version` to support future changes.

The application validates the complete tournament before accepting loaded data.

Saving uses a temporary file followed by `os.replace` to reduce the risk of leaving a partially written save file.

## 9. Reproducible demo simulation

The demo uses `random.Random(seed)` so a given seed produces repeatable results.

Demo data is saved separately from the user's active tournament to avoid accidentally overwriting real match records.

## 10. Testing strategy

Python's `unittest` framework tests the individual modules and the interactive CLI.

Tests cover normal operations, invalid inputs, persistence, and important edge cases.

## 11. Deployment decision

TournamentLab is a command-line application, not a web application.

GitHub is used for source-code hosting, collaboration, automated testing, and releases. GitHub Pages is not suitable for executing this Python CLI application.