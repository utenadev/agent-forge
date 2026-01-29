import unittest
from agent_forge import __version__


class TestVersion(unittest.TestCase):
    def test_version_is_defined(self):
        """Package should have a version defined"""
        self.assertIsNotNone(__version__)
        self.assertIsInstance(__version__, str)

    def test_version_format(self):
        """Version should follow semantic versioning format"""
        # Should match pattern like "0.1.0"
        parts = __version__.split(".")
        self.assertEqual(len(parts), 3)
        for part in parts:
            self.assertTrue(part.isdigit())


if __name__ == "__main__":
    unittest.main()
