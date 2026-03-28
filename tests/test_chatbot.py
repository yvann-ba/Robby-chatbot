"""Unit tests for Chatbot multi-provider LLM creation."""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# Mock all langchain dependencies before importing
_LANGCHAIN_MOCKS = {
    "langchain_openai": MagicMock(),
    "langchain_classic": MagicMock(),
    "langchain_classic.chains": MagicMock(),
    "langchain_core": MagicMock(),
    "langchain_core.prompts": MagicMock(),
    "langchain_community": MagicMock(),
    "langchain_community.callbacks": MagicMock(),
}


class TestChatbot(unittest.TestCase):
    """Test Chatbot provider-aware LLM creation."""

    def setUp(self):
        self.mock_st = MagicMock()
        self.mock_chatopenai_cls = MagicMock()
        mocks = {
            "streamlit": self.mock_st,
            **_LANGCHAIN_MOCKS,
        }
        mocks["langchain_openai"] = MagicMock(ChatOpenAI=self.mock_chatopenai_cls)
        self.patcher = patch.dict("sys.modules", mocks)
        self.patcher.start()
        sys.modules.pop("modules.chatbot", None)
        from modules.chatbot import Chatbot, MINIMAX_BASE_URL
        self.Chatbot = Chatbot
        self.MINIMAX_BASE_URL = MINIMAX_BASE_URL

    def tearDown(self):
        self.patcher.stop()
        os.environ.pop("MINIMAX_API_KEY", None)

    def test_default_provider_is_openai(self):
        bot = self.Chatbot("gpt-4o-mini", 0.5, MagicMock())
        self.assertEqual(bot.provider, "OpenAI")

    def test_minimax_provider(self):
        bot = self.Chatbot("MiniMax-M2.7", 0.5, MagicMock(), provider="MiniMax")
        self.assertEqual(bot.provider, "MiniMax")
        self.assertEqual(bot.model_name, "MiniMax-M2.7")

    def test_create_llm_openai(self):
        bot = self.Chatbot("gpt-4o", 0.7, MagicMock(), provider="OpenAI")
        bot._create_llm()
        self.mock_chatopenai_cls.assert_called_once_with(
            model_name="gpt-4o", temperature=0.7,
        )

    def test_create_llm_minimax(self):
        os.environ["MINIMAX_API_KEY"] = "test-key"
        bot = self.Chatbot("MiniMax-M2.7", 0.5, MagicMock(), provider="MiniMax")
        bot._create_llm()
        self.mock_chatopenai_cls.assert_called_once_with(
            model_name="MiniMax-M2.7", temperature=0.5,
            openai_api_key="test-key", openai_api_base=self.MINIMAX_BASE_URL,
        )

    def test_minimax_temperature_clamping(self):
        """MiniMax requires temperature > 0, so 0.0 should be clamped to 0.01."""
        os.environ["MINIMAX_API_KEY"] = "test-key"
        bot = self.Chatbot("MiniMax-M2.7", 0.0, MagicMock(), provider="MiniMax")
        bot._create_llm()
        call_kwargs = self.mock_chatopenai_cls.call_args[1]
        self.assertGreater(call_kwargs["temperature"], 0.0)
        self.assertAlmostEqual(call_kwargs["temperature"], 0.01)

    def test_openai_temperature_zero_allowed(self):
        bot = self.Chatbot("gpt-4o-mini", 0.0, MagicMock(), provider="OpenAI")
        bot._create_llm()
        call_kwargs = self.mock_chatopenai_cls.call_args[1]
        self.assertEqual(call_kwargs["temperature"], 0.0)

    def test_minimax_base_url(self):
        self.assertEqual(self.MINIMAX_BASE_URL, "https://api.minimax.io/v1")

    def test_chatbot_stores_vectors(self):
        v = MagicMock()
        bot = self.Chatbot("gpt-4o", 0.5, v)
        self.assertIs(bot.vectors, v)

    def test_highspeed_model(self):
        os.environ["MINIMAX_API_KEY"] = "test-key"
        bot = self.Chatbot("MiniMax-M2.7-highspeed", 0.3, MagicMock(), provider="MiniMax")
        bot._create_llm()
        call_kwargs = self.mock_chatopenai_cls.call_args[1]
        self.assertEqual(call_kwargs["model_name"], "MiniMax-M2.7-highspeed")


if __name__ == "__main__":
    unittest.main()
