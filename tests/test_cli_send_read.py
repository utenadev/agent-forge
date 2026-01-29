import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from click.testing import CliRunner

from agent_forge.cli import main


class TestCLISend(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("agent_forge.cli.send_command")
    @patch("agent_forge.cli.find_pane")
    @patch("agent_forge.cli.get_session")
    @patch("agent_forge.cli.load_config")
    def test_send_command_to_pane(self, mock_load, mock_get_session, mock_find, mock_send):
        """send command should send command to target pane"""
        mock_load.return_value = {"session_name": "forge-session"}

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        mock_pane = MagicMock()
        mock_find.return_value = mock_pane

        result = self.runner.invoke(main, ["send", "architect", "ls -la"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(mock_pane, "ls -la")

    @patch("agent_forge.cli.find_pane")
    @patch("agent_forge.cli.get_session")
    @patch("agent_forge.cli.load_config")
    def test_send_fails_if_session_not_found(self, mock_load, mock_get_session, mock_find):
        """send command should show error and exit gracefully if session not found"""
        mock_load.return_value = {"session_name": "forge-session"}
        mock_get_session.return_value = None

        result = self.runner.invoke(main, ["send", "architect", "ls -la"])
        self.assertEqual(result.exit_code, 0)  # Graceful exit
        self.assertIn("not found", result.output.lower())

    @patch("agent_forge.cli.get_session")
    @patch("agent_forge.cli.load_config")
    def test_send_fails_if_pane_not_found(self, mock_load, mock_get_session):
        """send command should show error and exit gracefully if pane not found"""
        mock_load.return_value = {"session_name": "forge-session"}

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        with patch("agent_forge.cli.find_pane", return_value=None):
            result = self.runner.invoke(main, ["send", "architect", "ls -la"])
            self.assertEqual(result.exit_code, 0)  # Graceful exit
            self.assertIn("not found", result.output.lower())


class TestCLIRead(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("agent_forge.cli.read_output")
    @patch("agent_forge.cli.find_pane")
    @patch("agent_forge.cli.get_session")
    @patch("agent_forge.cli.load_config")
    def test_read_output_from_pane(self, mock_load, mock_get_session, mock_find, mock_read):
        """read command should read output from target pane"""
        mock_load.return_value = {"session_name": "forge-session"}

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        mock_pane = MagicMock()
        mock_find.return_value = mock_pane

        mock_read.return_value = ["line1", "line2", "line3"]

        result = self.runner.invoke(main, ["read", "architect"])
        self.assertEqual(result.exit_code, 0)
        mock_read.assert_called_once_with(mock_pane, 100)
        self.assertIn("line1", result.output)

    @patch("agent_forge.cli.find_pane")
    @patch("agent_forge.cli.get_session")
    @patch("agent_forge.cli.load_config")
    def test_read_fails_if_session_not_found(self, mock_load, mock_get_session, mock_find):
        """read command should fail if session not found"""
        mock_load.return_value = {"session_name": "forge-session"}
        mock_get_session.return_value = None

        result = self.runner.invoke(main, ["read", "architect"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("not found", result.output.lower())


class TestCLIStart(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("agent_forge.cli.start_forge")
    @patch("agent_forge.cli.config_exists")
    @patch("agent_forge.cli.load_config")
    def test_start_with_config(self, mock_load, mock_exists, mock_start):
        """start command should start forge with config"""
        mock_exists.return_value = True
        mock_load.return_value = {"session_name": "forge-session"}

        mock_session = MagicMock()
        mock_session.name = "forge-session"
        mock_start.return_value = mock_session

        result = self.runner.invoke(main, ["start"])
        self.assertEqual(result.exit_code, 0)
        mock_start.assert_called_once()

    @patch("agent_forge.cli.config_exists")
    def test_start_fails_without_config(self, mock_exists):
        """start command should fail if .forge.yaml does not exist"""
        mock_exists.return_value = False

        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            result = self.runner.invoke(main, ["start"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("not found", result.output.lower())


if __name__ == "__main__":
    unittest.main()
