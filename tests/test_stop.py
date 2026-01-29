import unittest
from unittest.mock import MagicMock, patch
from click.testing import CliRunner

from agent_forge.cli import main
from agent_forge.session import stop_session


class TestStopSession(unittest.TestCase):
    @patch("agent_forge.session.get_session")
    def test_stop_session_kills_session(self, mock_get_session):
        """stop_session should kill the session"""
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        _ = stop_session("test-session")
        mock_session.kill.assert_called_once()

    @patch("agent_forge.session.get_session")
    def test_stop_session_returns_none_if_not_found(self, mock_get_session):
        """stop_session should return None if session not found"""
        mock_get_session.return_value = None

        result = stop_session("test-session")
        self.assertIsNone(result)


class TestCLIStop(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("agent_forge.cli.stop_session")
    @patch("agent_forge.cli.load_config")
    @patch("agent_forge.cli.config_exists")
    def test_stop_with_session_name(self, mock_exists, mock_load, mock_stop):
        """stop command should stop specified session"""
        mock_exists.return_value = True
        mock_load.return_value = {"session_name": "test-session"}
        mock_stop.return_value = MagicMock()

        result = self.runner.invoke(main, ["stop", "--session-name", "my-session"])
        self.assertEqual(result.exit_code, 0)
        mock_stop.assert_called_once()

    @patch("agent_forge.cli.stop_session")
    @patch("agent_forge.cli.load_config")
    @patch("agent_forge.cli.config_exists")
    def test_stop_uses_default_session(self, mock_exists, mock_load, mock_stop):
        """stop command should use default session from config"""
        mock_exists.return_value = True
        mock_load.return_value = {"session_name": "forge-session"}
        mock_stop.return_value = MagicMock()

        result = self.runner.invoke(main, ["stop"])
        self.assertEqual(result.exit_code, 0)
        mock_stop.assert_called_once_with("forge-session")

    @patch("agent_forge.cli.stop_session")
    @patch("agent_forge.cli.load_config")
    @patch("agent_forge.cli.config_exists")
    def test_stop_handles_session_not_found(self, mock_exists, mock_load, mock_stop):
        """stop command should handle session not found gracefully"""
        mock_exists.return_value = True
        mock_load.return_value = {"session_name": "forge-session"}
        mock_stop.return_value = None

        result = self.runner.invoke(main, ["stop"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("not found", result.output.lower())

    @patch("agent_forge.cli.config_exists")
    def test_stop_fails_without_config(self, mock_exists):
        """stop command should fail if .forge.yaml does not exist"""
        mock_exists.return_value = False

        result = self.runner.invoke(main, ["stop"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("not found", result.output.lower())


if __name__ == "__main__":
    unittest.main()
