import unittest
from unittest.mock import MagicMock, patch

from agent_forge.actions import send_command, read_output


class TestSendCommand(unittest.TestCase):
    def test_send_command_calls_send_keys(self):
        """send_command should call pane.send_keys with the command"""
        mock_pane = MagicMock()
        send_command(mock_pane, "ls -la")
        mock_pane.send_keys.assert_called_once_with("ls -la")

    def test_send_command_returns_none(self):
        """send_command should return None (fire and forget)"""
        mock_pane = MagicMock()
        result = send_command(mock_pane, "echo test")
        self.assertIsNone(result)


class TestReadOutput(unittest.TestCase):
    def test_read_output_calls_capture_pane(self):
        """read_output should call pane.capture_pane with correct lines"""
        mock_pane = MagicMock()
        mock_pane.capture_pane.return_value = ["line1", "line2", "line3"]

        result = read_output(mock_pane, lines=100)
        mock_pane.capture_pane.assert_called_once_with(start=-100)

    def test_read_output_returns_captured_lines(self):
        """read_output should return the captured output as list"""
        mock_pane = MagicMock()
        expected = ["line1", "line2", "line3"]
        mock_pane.capture_pane.return_value = expected

        result = read_output(mock_pane)
        self.assertEqual(result, expected)

    def test_read_output_default_lines(self):
        """read_output should default to 100 lines"""
        mock_pane = MagicMock()
        read_output(mock_pane)
        mock_pane.capture_pane.assert_called_once_with(start=-100)


if __name__ == "__main__":
    unittest.main()
