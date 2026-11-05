
# TournamentLab — AI Learning Log

## Project learning objectives

Develop practical Python skills through the design and implementation of a command-line esports league manager.

## Key concepts practised

### 1. Data structures and types

- Used lists to manage teams and fixtures.
- Used dictionaries to represent structured records.
- Applied strings, integers, booleans, and `None`.
- Used stable IDs to connect teams and fixtures.

### 2. Functions and modular design

- Broke the application into small, focused functions.
- Practised parameters, arguments, and return values.
- Separated business logic from user interaction.
- Learned why reusable functions improve maintainability.

### 3. Validation and defensive programming

- Validated team names and duplicate registrations.
- Rejected negative, fractional, and boolean scores.
- Learned that Python considers `bool` a subclass of `int`.
- Validated data before modifying records.

### 4. Algorithms and problem-solving

- Used combinations to generate unique team pairings.
- Applied the round-robin fixture formula.
- Calculated played matches, wins, draws, losses, and points.
- Calculated goal difference as goals scored minus goals conceded.
- Applied deterministic ranking rules.

### 5. Persistence and data integrity

- Saved tournament records in JSON.
- Loaded and validated saved data.
- Learned the difference between valid JSON syntax and valid application data.
- Used schema versioning and atomic file replacement.

### 6. Testing and debugging

- Wrote automated tests using `unittest`.
- Tested successful operations and invalid inputs.
- Tested that invalid results do not mutate fixtures.
- Tested save-and-load behaviour.
- Tested CLI workflows using simulated user input.

### 7. Reproducibility

- Used a seeded random generator for demo results.
- Confirmed that the same seed produces the same results.
- Kept simulated data separate from the active tournament.

## How AI supported the learning process

AI was used as a learning and development assistant to:

- Explain unfamiliar Python concepts.
- Review implementation approaches.
- Help identify edge cases.
- Suggest test scenarios.
- Explain errors and improve code structure.
- Support documentation and project planning.

The goal was to understand the underlying logic, review suggestions critically, and verify implementation through execution and automated tests.

## Areas for further improvement

- Expand tests for all ranking tie-breakers.
- Improve CLI handling of unexpected end-of-input.
- Add tournament editing through a safe, validated workflow.
- Consider additional export formats.
- Explore a web interface in a future version.

## Reflection

This project strengthened my understanding of how separate Python modules work together to form a complete application.

I gained practical experience in data modelling, validation, algorithms, persistence, automated testing, and command-line interaction.

The most important lesson was that a working application requires more than code that runs: it also needs predictable behaviour, data integrity, and tests that verify its requirements.