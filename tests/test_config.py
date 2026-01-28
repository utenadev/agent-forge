import tempfile
import unittest
from pathlib import Path

from agent_forge.config import (
    DEFAULT_FORGE_CONFIG,
    FORGE_CONFIG_FILE,
    config_exists,
    load_config,
    write_default_config,
)


class TestConfigConstants(unittest.TestCase):
    def test_forge_config_file_name(self):
        """Default config file name should be .forge.yaml"""
        self.assertEqual(FORGE_CONFIG_FILE, ".forge.yaml")

    def test_default_config_is_not_empty(self):
        """Default config template should not be empty"""
        self.assertIsNotNone(DEFAULT_FORGE_CONFIG)
        self.assertGreater(len(DEFAULT_FORGE_CONFIG), 0)


class TestConfigExists(unittest.TestCase):
    def test_config_not_exists_in_empty_dir(self):
        """Should return False when config does not exist"""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = config_exists(tmpdir)
            self.assertFalse(result)

    def test_config_exists_when_file_present(self):
        """Should return True when config file exists"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / FORGE_CONFIG_FILE
            config_path.write_text("test: data")
            result = config_exists(tmpdir)
            self.assertTrue(result)


class TestWriteDefaultConfig(unittest.TestCase):
    def test_write_default_config(self):
        """Should write default config to specified directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            write_default_config(tmpdir)
            config_path = Path(tmpdir) / FORGE_CONFIG_FILE
            self.assertTrue(config_path.exists())
            content = config_path.read_text()
            self.assertEqual(content, DEFAULT_FORGE_CONFIG)

    def test_write_default_config_fails_if_exists(self):
        """Should raise error if config already exists"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / FORGE_CONFIG_FILE
            config_path.write_text("existing: config")
            with self.assertRaises(FileExistsError):
                write_default_config(tmpdir)


class TestLoadConfig(unittest.TestCase):
    def test_load_valid_yaml_config(self):
        """Should load valid YAML config"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / FORGE_CONFIG_FILE
            config_path.write_text(DEFAULT_FORGE_CONFIG)
            config = load_config(tmpdir)
            self.assertIsInstance(config, dict)
            self.assertIn("session_name", config)
            self.assertIn("windows", config)

    def test_load_config_returns_none_if_not_exists(self):
        """Should return None if config does not exist"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = load_config(tmpdir)
            self.assertIsNone(config)


class TestDefaultConfigStructure(unittest.TestCase):
    def test_default_config_is_valid_yaml(self):
        """Default config should be valid YAML"""
        import yaml
        try:
            yaml.safe_load(DEFAULT_FORGE_CONFIG)
        except yaml.YAMLError as e:
            self.fail(f"Default config is not valid YAML: {e}")

    def test_default_config_has_session_name(self):
        """Default config should have session_name"""
        import yaml
        config = yaml.safe_load(DEFAULT_FORGE_CONFIG)
        self.assertIn("session_name", config)
        self.assertIsInstance(config["session_name"], str)

    def test_default_config_has_windows(self):
        """Default config should have windows array"""
        import yaml
        config = yaml.safe_load(DEFAULT_FORGE_CONFIG)
        self.assertIn("windows", config)
        self.assertIsInstance(config["windows"], list)

    def test_default_config_has_three_panes(self):
        """Default config should have 3 windows (Architect, Implementer, Reviewer)"""
        import yaml
        config = yaml.safe_load(DEFAULT_FORGE_CONFIG)
        self.assertEqual(len(config["windows"]), 3)
        window_names = [w.get("window_name") for w in config["windows"]]
        self.assertIn("architect", window_names)
        self.assertIn("implementer", window_names)
        self.assertIn("reviewer", window_names)


if __name__ == "__main__":
    unittest.main()
