
"""Automated tests for the TournamentLab command-line interface."""

import tempfile
import unittest
from pathlib import Path

from tournament.cli import run_cli


class TestTournamentCLI(unittest.TestCase):

    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temporary_directory.name) / "tournament.json"
        self.output = []

    def tearDown(self):
        self.temporary_directory.cleanup()

    def run_application(self, commands):
        """Run the CLI using a sequence of simulated user inputs."""

        remaining_commands = iter(commands)

        def fake_input(prompt=""):
            return next(remaining_commands)

        def capture_output(message=""):
            self.output.append(str(message))

        run_cli(
            data_file=self.data_file,
            input_fn=fake_input,
            output_fn=capture_output,
        )

    def test_register_teams_and_generate_fixtures(self):
        self.run_application([
            "1", "Thunder",
            "1", "Comets",
            "1", "Phoenix",
            "1", "Rockets",
            "3",
            "9",
        ])

        self.assertTrue(self.data_file.exists())
        self.assertTrue(
            any("Generated 6 fixtures." in line for line in self.output)
        )

    def test_result_is_saved_and_survives_reload(self):
        self.run_application([
            "1", "Thunder",
            "1", "Comets",
            "1", "Phoenix",
            "1", "Rockets",
            "3",
            "5", "M001", "3", "1",
            "9",
        ])

        self.output.clear()

        self.run_application([
            "8",
            "4",
            "6",
            "9",
        ])

        self.assertTrue(
            any(
                "Thunder vs Comets | 3 - 1" in line
                for line in self.output
            )
        )

        self.assertTrue(
            any("Thunder" in line and "3" in line for line in self.output)
        )

    def test_fewer_than_four_teams_cannot_generate_fixtures(self):
        self.run_application([
            "1", "Thunder",
            "1", "Comets",
            "1", "Phoenix",
            "3",
            "9",
        ])

        self.assertFalse(self.data_file.exists())

        self.assertTrue(
            any(
                "between 4 and 8 teams" in line
                for line in self.output
            )
        )

    def test_unknown_fixture_is_rejected(self):
        self.run_application([
            "1", "Thunder",
            "1", "Comets",
            "1", "Phoenix",
            "1", "Rockets",
            "3",
            "5", "M999",
            "9",
        ])

        self.assertTrue(
            any("Fixture not found." in line for line in self.output)
        )

    def test_invalid_score_is_not_recorded(self):
        self.run_application([
            "1", "Thunder",
            "1", "Comets",
            "1", "Phoenix",
            "1", "Rockets",
            "3",
            "5", "M001", "-1", "2",
            "9",
        ])

        self.output.clear()

        self.run_application([
            "8",
            "4",
            "9",
        ])

        self.assertTrue(
            any(
                "M001: Thunder vs Comets | Pending" in line
                for line in self.output
            )
        )

    def test_invalid_menu_choice_is_handled(self):
        self.run_application([
            "invalid",
            "9",
        ])

        self.assertTrue(
            any(
                "Invalid choice" in line
                for line in self.output
            )
        )

    def test_loaded_tournament_replaces_active_data(self):
        self.run_application([
            "1", "Thunder",
            "1", "Comets",
            "1", "Phoenix",
            "1", "Rockets",
            "3",
            "9",
        ])

        self.output.clear()

        self.run_application([
            "8",
            "2",
            "9",
        ])

        self.assertTrue(
            any("TM001 - Thunder" in line for line in self.output)
        )

        self.assertTrue(
            any("TM004 - Rockets" in line for line in self.output)
        )


if __name__ == "__main__":
    unittest.main()