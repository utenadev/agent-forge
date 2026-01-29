import unittest
from unittest.mock import MagicMock, patch
from click.testing import CliRunner

from agent_forge.cli import main


class TestErrorHandling(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("agent_forge.cli.get_session")
    @patch("agent_forge.cli.load_config")
    @patch("agent_forge.cli.config_exists")
    def test_send_shows_available_panes(self, mock_exists, mock_load, mock_get_session):
        """send command should show available panes when target not found"""
        mock_exists.return_value = True
        mock_load.return_value = {"session_name": "forge-session"}

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        # Mock windows and panes
        mock_window1 = MagicMock()
        mock_window1.window_name = "architect"
        mock_window1.panes = [MagicMock()]

        mock_window2 = MagicMock()
        mock_window2.window_name = "implementer"
        mock_window2.panes = [MagicMock()]

        mock_window3 = MagicMock()
        mock_window3.window_name = "reviewer"
        mock_window3.panes = [MagicMock()]

        mock_session.windows = [mock_window1, mock_window2, mock_window3]

        from agent_forge.cli import find_pane
        with patch("agent_forge.cli.find_pane", return_value=None):
            result = self.runner.invoke(main, ["send", "unknown", "test"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("not found", result.output.lower())
        self.assertIn("architect", result.output.lower())
        self.assertIn("implementer", result.output.lower())
        self.assertIn("reviewer", result.output.lower())

    @patch("agent_forge.cli.get_session")
    @patch("agent_forge.cli.load_config")
    @patch("agent_forge.cli.config_exists")
    def test_read_shows_available_panes(self, mock_exists, mock_load, mock_get_session):
        """read command should show available panes when target not found"""
        mock_exists.return_value = True
        mock_load.return_value = {"session_name": "forge-session"}

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        # Mock windows and panes
        mock_window1 = MagicMock()
        mock_window1.window_name = "architect"
        mock_window1.panes = [MagicMock()]

        mock_window2 = MagicMock()
        mock_window2.window_name = "implementer"
        mock_window2.panes = [MagicMock()]

        mock_window3 = MagicMock()
        mock_window3.window_name = "reviewer"
        mock_window3.panes = [MagicMock()]

        mock_session.windows = [mock_window1, mock_window2, mock_window3]

        from agent_forge.cli import find_pane
        with patch("agent_forge.cli.find_pane", return_value=None):
            result = self.runner.invoke(main, ["read", "unknown"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("not found", result.output.lower())
        self.assertIn("architect", result.output.lower())
        self.assertIn("implementer", result.output.lower())
        self.assertIn("reviewer", result.output.lower())


if __name__ == "__main__":
    unittest.main()
