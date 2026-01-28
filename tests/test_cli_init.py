import os
import tempfile
import unittest
from pathlib import Path
from click.testing import CliRunner

from agent_forge.cli import main


class TestCLIInit(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_init_creates_forge_yaml(self):
        """init command should create .forge.yaml file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            result = self.runner.invoke(main, ["init"])
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(Path(".forge.yaml").exists())

    def test_init_shows_success_message(self):
        """init command should show success message"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            result = self.runner.invoke(main, ["init"])
            self.assertEqual(result.exit_code, 0)
            self.assertIn("created", result.output.lower())

    def test_init_fails_if_config_exists(self):
        """init command should fail if .forge.yaml already exists"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            # Create existing config
            Path(".forge.yaml").write_text("existing: config")
            result = self.runner.invoke(main, ["init"])
            self.assertNotEqual(result.exit_code, 0)
            self.assertIn("already exists", result.output.lower())

    def test_init_with_overwrite_flag(self):
        """init --force should overwrite existing config"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            # Create existing config
            Path(".forge.yaml").write_text("old: config")
            result = self.runner.invoke(main, ["init", "--force"])
            self.assertEqual(result.exit_code, 0)
            content = Path(".forge.yaml").read_text()
            self.assertNotEqual(content, "old: config")
            self.assertIn("session_name", content)


if __name__ == "__main__":
    unittest.main()
