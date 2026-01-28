import unittest
from unittest.mock import MagicMock, patch, mock_open

from agent_forge.session import get_session, find_pane, start_forge


class TestGetSession(unittest.TestCase):
    @patch("agent_forge.session.Server")
    def test_get_session_returns_matching_session(self, mock_server_class):
        """get_session should return the session with matching name"""
        mock_session = MagicMock()
        mock_session.name = "forge-session"
        mock_server = MagicMock()
        mock_server.sessions = [mock_session]
        mock_server_class.return_value = mock_server

        result = get_session("forge-session")
        self.assertEqual(result, mock_session)

    @patch("agent_forge.session.Server")
    def test_get_session_returns_none_if_not_found(self, mock_server_class):
        """get_session should return None if no matching session exists"""
        mock_session = MagicMock()
        mock_session.name = "other-session"
        mock_server = MagicMock()
        mock_server.sessions = [mock_session]
        mock_server_class.return_value = mock_server

        result = get_session("forge-session")
        self.assertIsNone(result)


class TestFindPane(unittest.TestCase):
    def test_find_pane_by_window_name(self):
        """find_pane should find pane by window_name"""
        mock_pane = MagicMock()
        mock_window = MagicMock()
        mock_window.window_name = "architect"
        mock_window.panes = [mock_pane]
        mock_session = MagicMock()
        mock_session.windows = [mock_window]

        result = find_pane(mock_session, "architect")
        self.assertEqual(result, mock_pane)

    def test_find_pane_returns_none_if_not_found(self):
        """find_pane should return None if no matching window exists"""
        mock_window = MagicMock()
        mock_window.window_name = "implementer"
        mock_session = MagicMock()
        mock_session.windows = [mock_window]

        result = find_pane(mock_session, "architect")
        self.assertIsNone(result)

    def test_find_pane_returns_first_pane_of_window(self):
        """find_pane should return the first pane of the matching window"""
        mock_pane1 = MagicMock()
        mock_pane2 = MagicMock()
        mock_window = MagicMock()
        mock_window.window_name = "architect"
        mock_window.panes = [mock_pane1, mock_pane2]
        mock_session = MagicMock()
        mock_session.windows = [mock_window]

        result = find_pane(mock_session, "architect")
        self.assertEqual(result, mock_pane1)

    def test_find_pane_case_insensitive(self):
        """find_pane should match window names case-insensitively"""
        mock_pane = MagicMock()
        mock_window = MagicMock()
        mock_window.window_name = "Architect"
        mock_window.panes = [mock_pane]
        mock_session = MagicMock()
        mock_session.windows = [mock_window]

        result = find_pane(mock_session, "architect")
        self.assertEqual(result, mock_pane)


class TestStartForge(unittest.TestCase):
    @patch("agent_forge.session.WorkspaceBuilder")
    @patch("agent_forge.session.yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    def test_start_forge_loads_workspace(self, mock_file, mock_yaml_load, mock_builder_class):
        """start_forge should load workspace from config path"""
        config_path = "/path/to/.forge.yaml"
        mock_config = {"session_name": "forge-session", "windows": []}
        mock_yaml_load.return_value = mock_config

        mock_builder = MagicMock()
        mock_builder_class.return_value = mock_builder

        mock_server = MagicMock()
        mock_session = MagicMock()

        with patch("agent_forge.session.Server", return_value=mock_server):
            mock_server.find_where.return_value = mock_session
            result = start_forge(config_path, attach=False)

        mock_builder.build.assert_called_once()
        mock_server.find_where.assert_called_once_with({"session_name": "forge-session"})

    @patch("agent_forge.session.WorkspaceBuilder")
    @patch("agent_forge.session.yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    def test_start_forge_with_session_name(self, mock_file, mock_yaml_load, mock_builder_class):
        """start_forge should override session name"""
        config_path = "/path/to/.forge.yaml"
        mock_config = {"session_name": "default-session", "windows": []}
        mock_yaml_load.return_value = mock_config

        mock_builder = MagicMock()
        mock_builder_class.return_value = mock_builder

        mock_server = MagicMock()
        mock_session = MagicMock()

        with patch("agent_forge.session.Server", return_value=mock_server):
            mock_server.find_where.return_value = mock_session
            result = start_forge(config_path, session_name="my-session", attach=False)

        # Should override session name
        mock_server.find_where.assert_called_once_with({"session_name": "my-session"})


if __name__ == "__main__":
    unittest.main()
