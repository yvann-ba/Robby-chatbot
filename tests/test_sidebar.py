"""Unit tests for multi-provider Sidebar."""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add src to path for imports
_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


class TestSidebar(unittest.TestCase):
    """Test provider and model selection in Sidebar."""

    def setUp(self):
        self.patcher = patch.dict("sys.modules", {"streamlit": MagicMock()})
        self.patcher.start()
        # Force reimport
        sys.modules.pop("modules.sidebar", None)
        from modules.sidebar import Sidebar
        self.Sidebar = Sidebar

    def tearDown(self):
        self.patcher.stop()

    def test_provider_options_exist(self):
        self.assertIn("OpenAI", self.Sidebar.PROVIDER_OPTIONS)
        self.assertIn("MiniMax", self.Sidebar.PROVIDER_OPTIONS)

    def test_provider_models_openai(self):
        models = self.Sidebar.PROVIDER_MODELS["OpenAI"]
        self.assertIn("gpt-4o-mini", models)
        self.assertIn("gpt-4o", models)

    def test_provider_models_minimax(self):
        models = self.Sidebar.PROVIDER_MODELS["MiniMax"]
        self.assertIn("MiniMax-M2.7", models)
        self.assertIn("MiniMax-M2.7-highspeed", models)

    def test_openai_is_default_provider(self):
        self.assertEqual(self.Sidebar.PROVIDER_OPTIONS[0], "OpenAI")

    def test_each_provider_has_models(self):
        for provider in self.Sidebar.PROVIDER_OPTIONS:
            self.assertIn(provider, self.Sidebar.PROVIDER_MODELS)
            self.assertTrue(len(self.Sidebar.PROVIDER_MODELS[provider]) > 0)

    def test_temperature_range(self):
        self.assertEqual(self.Sidebar.TEMPERATURE_MIN_VALUE, 0.0)
        self.assertEqual(self.Sidebar.TEMPERATURE_MAX_VALUE, 1.0)


if __name__ == "__main__":
    unittest.main()
