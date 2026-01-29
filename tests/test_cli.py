import unittest
from click.testing import CliRunner
from agent_forge.cli import main


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_cli_main_exists(self):
        """CLI main entry point should exist"""
        result = self.runner.invoke(main, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("agent", result.output.lower())
        self.assertIn("forge", result.output.lower())

    def test_init_command_exists(self):
        """init command should exist"""
        result = self.runner.invoke(main, ["init", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("init", result.output.lower())

    def test_start_command_exists(self):
        """start command should exist"""
        result = self.runner.invoke(main, ["start", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("start", result.output.lower())

    def test_send_command_exists(self):
        """send command should exist"""
        result = self.runner.invoke(main, ["send", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("send", result.output.lower())

    def test_read_command_exists(self):
        """read command should exist"""
        result = self.runner.invoke(main, ["read", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("read", result.output.lower())

    def test_list_command_exists(self):
        """list command should exist"""
        result = self.runner.invoke(main, ["list", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("list", result.output.lower())


if __name__ == "__main__":
    unittest.main()
