"""E2E tests with live tmux sessions."""

import os
import tempfile
import unittest
from pathlib import Path

from libtmux import Server

from agent_forge.session import get_session, find_pane, stop_session
from agent_forge.actions import send_command, read_output


class TestLiveTmux(unittest.TestCase):
    """E2E tests that require actual tmux server."""

    def setUp(self):
        """Set up test session."""
        self.server = Server()
        self.session_name = "test-forge-e2e"

    def tearDown(self):
        """Clean up test session."""
        session = stop_session(self.session_name)

    def test_e2e_start_send_read_stop(self):
        """E2E test: create session, send command, read output, stop session."""
        # 1. Create session using libtmux directly
        session = self.server.new_session(
            session_name=self.session_name,
            attach=False,
        )

        # Create windows
        architect_window = session.new_window(
            window_name="architect",
            attach=False,
        )
        implementer_window = session.new_window(
            window_name="implementer",
            attach=False,
        )

        self.assertIsNotNone(session)
        self.assertEqual(session.name, self.session_name)

        # 2. Find pane
        pane = find_pane(session, "architect")
        self.assertIsNotNone(pane)

        # 3. Send command
        send_command(pane, "echo 'Hello E2E'")

        # 4. Read output (need to wait a bit for command to execute)
        import time
        time.sleep(0.5)  # Give tmux time to process the command

        output = read_output(pane, lines=100)
        output_text = "\n".join(output)

        # 5. Verify output contains our test string
        self.assertIn("Hello E2E", output_text)

        # 6. Stop session (done in tearDown)
        session = stop_session(self.session_name)
        self.assertIsNotNone(session)

    def test_e2e_find_pane_case_insensitive(self):
        """E2E test: find_pane should be case-insensitive."""
        # Create session
        session = self.server.new_session(
            session_name=self.session_name,
            attach=False,
        )
        session.new_window(window_name="architect", attach=False)

        # Should find pane regardless of case
        pane_lower = find_pane(session, "architect")
        pane_upper = find_pane(session, "ARCHITECT")
        pane_mixed = find_pane(session, "ArChItEcT")

        self.assertIsNotNone(pane_lower)
        self.assertIsNotNone(pane_upper)
        self.assertIsNotNone(pane_mixed)

        # All should reference the same pane
        self.assertEqual(pane_lower, pane_upper)
        self.assertEqual(pane_upper, pane_mixed)


if __name__ == "__main__":
    unittest.main()
