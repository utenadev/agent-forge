"""Tests for the enhanced forge list command."""

import unittest
from unittest.mock import MagicMock, patch
from click.testing import CliRunner

from agent_forge.cli import main


class TestCLIList(unittest.TestCase):
    """Tests for the list command with detailed tabular output."""

    def setUp(self):
        self.runner = CliRunner()

    @patch("libtmux.Server")
    def test_list_shows_tabular_output(self, mock_server_class):
        """list command should show tabular output with SESSION, WINDOW, PANE, TITLE, CURRENT CMD"""
        # Create mock server with sessions
        mock_server = MagicMock()
        mock_server_class.return_value = mock_server

        # Create mock session
        mock_session = MagicMock()
        mock_session.name = "forge-session"
        mock_server.sessions = [mock_session]

        # Create mock windows with panes
        mock_window1 = MagicMock()
        mock_window1.window_name = "architect"
        mock_window1.id = 1

        mock_pane1 = MagicMock()
        mock_pane1.id = 1
        mock_pane1.pane_title = "Gemini"
        mock_pane1.current_command = "nvim"

        mock_window1.panes = [mock_pane1]

        mock_window2 = MagicMock()
        mock_window2.window_name = "implementer"
        mock_window2.id = 2

        mock_pane2 = MagicMock()
        mock_pane2.id = 2
        mock_pane2.pane_title = "Implementer"
        mock_pane2.current_command = "python"

        mock_window2.panes = [mock_pane2]

        mock_session.windows = [mock_window1, mock_window2]

        result = self.runner.invoke(main, ["list"])

        self.assertEqual(result.exit_code, 0)
        # Check for table headers
        output = result.output
        self.assertIn("SESSION", output)
        self.assertIn("WINDOW", output)
        self.assertIn("PANE", output)
        self.assertIn("TITLE", output)
        self.assertIn("CURRENT CMD", output)
        # Check for data
        self.assertIn("forge-session", output)
        self.assertIn("architect", output)
        self.assertIn("implementer", output)

    @patch("libtmux.Server")
    def test_list_handles_no_sessions_gracefully(self, mock_server_class):
        """list command should show message when no sessions exist"""
        mock_server = MagicMock()
        mock_server_class.return_value = mock_server
        mock_server.sessions = []

        result = self.runner.invoke(main, ["list"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("no active sessions", result.output.lower())

    @patch("libtmux.Server")
    def test_list_groups_by_session_and_window(self, mock_server_class):
        """list command should group output by Session, then Window"""
        mock_server = MagicMock()
        mock_server_class.return_value = mock_server

        # Create two sessions
        mock_session1 = MagicMock()
        mock_session1.name = "forge-session"

        mock_window1 = MagicMock()
        mock_window1.window_name = "architect"
        mock_window1.id = 1
        mock_pane1 = MagicMock()
        mock_pane1.id = 1
        mock_pane1.pane_title = "Gemini"
        mock_pane1.current_command = "nvim"
        mock_window1.panes = [mock_pane1]

        mock_session1.windows = [mock_window1]

        mock_session2 = MagicMock()
        mock_session2.name = "another-session"

        mock_window2 = MagicMock()
        mock_window2.window_name = "worker"
        mock_window2.id = 1
        mock_pane2 = MagicMock()
        mock_pane2.id = 1
        mock_pane2.pane_title = "Worker"
        mock_pane2.current_command = "bash"
        mock_window2.panes = [mock_pane2]

        mock_session2.windows = [mock_window2]

        mock_server.sessions = [mock_session1, mock_session2]

        result = self.runner.invoke(main, ["list"])

        self.assertEqual(result.exit_code, 0)
        output = result.output
        # Both sessions should appear
        self.assertIn("forge-session", output)
        self.assertIn("another-session", output)


if __name__ == "__main__":
    unittest.main()
