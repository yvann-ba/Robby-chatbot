"""
Integration tests for MiniMax provider support.
These tests verify the end-to-end provider wiring without hitting real APIs.
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

_ALL_MOCKS = {
    "streamlit": MagicMock(),
    "pdfplumber": MagicMock(),
    "pandas": MagicMock(),
    "langchain_openai": MagicMock(),
    "langchain_classic": MagicMock(),
    "langchain_classic.chains": MagicMock(),
    "langchain_core": MagicMock(),
    "langchain_core.prompts": MagicMock(),
    "langchain_community": MagicMock(),
    "langchain_community.callbacks": MagicMock(),
    "langchain_community.document_loaders": MagicMock(),
    "langchain_community.vectorstores": MagicMock(),
    "langchain_text_splitters": MagicMock(),
}


class TestMiniMaxProviderIntegration(unittest.TestCase):
    """Integration test: Sidebar -> Chatbot -> LLM creation pipeline."""

    def setUp(self):
        self.mock_chatopenai_cls = MagicMock()
        mocks = {
            **_ALL_MOCKS,
            "langchain_openai": MagicMock(ChatOpenAI=self.mock_chatopenai_cls),
        }
        self.patcher = patch.dict("sys.modules", mocks)
        self.patcher.start()
        for mod in ["modules.sidebar", "modules.chatbot", "modules.embedder", "modules.utils"]:
            sys.modules.pop(mod, None)

    def tearDown(self):
        self.patcher.stop()
        os.environ.pop("MINIMAX_API_KEY", None)

    def test_minimax_end_to_end_llm_creation(self):
        """Verify selecting MiniMax provider creates LLM with correct base URL."""
        from modules.sidebar import Sidebar
        from modules.chatbot import Chatbot

        os.environ["MINIMAX_API_KEY"] = "eyJ-integration-test"

        minimax_models = Sidebar.PROVIDER_MODELS["MiniMax"]
        self.assertIn("MiniMax-M2.7", minimax_models)

        bot = Chatbot("MiniMax-M2.7", 0.5, MagicMock(), provider="MiniMax")
        bot._create_llm()

        call_kwargs = self.mock_chatopenai_cls.call_args[1]
        self.assertEqual(call_kwargs["model_name"], "MiniMax-M2.7")
        self.assertEqual(call_kwargs["openai_api_base"], "https://api.minimax.io/v1")
        self.assertEqual(call_kwargs["openai_api_key"], "eyJ-integration-test")
        self.assertEqual(call_kwargs["temperature"], 0.5)

    def test_openai_end_to_end_llm_creation(self):
        """Verify OpenAI provider still works as default."""
        from modules.chatbot import Chatbot

        bot = Chatbot("gpt-4o-mini", 0.0, MagicMock(), provider="OpenAI")
        bot._create_llm()

        call_kwargs = self.mock_chatopenai_cls.call_args[1]
        self.assertEqual(call_kwargs["model_name"], "gpt-4o-mini")
        self.assertEqual(call_kwargs["temperature"], 0.0)
        self.assertNotIn("openai_api_base", call_kwargs)

    def test_provider_model_consistency(self):
        """Verify all provider models in Sidebar are valid strings."""
        from modules.sidebar import Sidebar

        for provider, models in Sidebar.PROVIDER_MODELS.items():
            for model in models:
                self.assertIsInstance(model, str)
                self.assertTrue(len(model) > 0, f"Empty model name for {provider}")


class TestApiKeyEnvIntegration(unittest.TestCase):
    """Integration test: API key env var setting per provider."""

    def setUp(self):
        self.mock_st = MagicMock()
        self.mock_chatopenai_cls = MagicMock()
        mocks = {
            **_ALL_MOCKS,
            "streamlit": self.mock_st,
            "langchain_openai": MagicMock(ChatOpenAI=self.mock_chatopenai_cls),
        }
        self.patcher = patch.dict("sys.modules", mocks)
        self.patcher.start()
        for mod in ["modules.utils", "modules.chatbot", "modules.embedder"]:
            sys.modules.pop(mod, None)

    def tearDown(self):
        self.patcher.stop()
        for k in ["MINIMAX_API_KEY", "OPENAI_API_KEY"]:
            os.environ.pop(k, None)

    def test_minimax_key_then_chatbot(self):
        """Set MiniMax key via Utilities, then create Chatbot with it."""
        from modules.utils import Utilities
        from modules.chatbot import Chatbot

        self.mock_st.session_state = {"provider": "MiniMax"}
        Utilities.set_api_key_env("eyJ-full-flow")
        self.assertEqual(os.environ["MINIMAX_API_KEY"], "eyJ-full-flow")

        bot = Chatbot("MiniMax-M2.7-highspeed", 0.3, MagicMock(), provider="MiniMax")
        self.assertEqual(bot.provider, "MiniMax")
        self.assertEqual(bot.model_name, "MiniMax-M2.7-highspeed")


if __name__ == "__main__":
    unittest.main()
