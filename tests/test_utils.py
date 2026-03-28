"""Unit tests for Utilities multi-provider API key handling."""
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


class TestUtilitiesSetApiKeyEnv(unittest.TestCase):
    """Test set_api_key_env for different providers."""

    def setUp(self):
        self.mock_st = MagicMock()
        mocks = {**_ALL_MOCKS, "streamlit": self.mock_st}
        self.patcher = patch.dict("sys.modules", mocks)
        self.patcher.start()
        for mod in ["modules.utils", "modules.chatbot", "modules.embedder"]:
            sys.modules.pop(mod, None)
        from modules.utils import Utilities
        self.Utilities = Utilities

    def tearDown(self):
        self.patcher.stop()
        for key in ["MINIMAX_API_KEY", "OPENAI_API_KEY"]:
            os.environ.pop(key, None)

    def test_set_openai_key(self):
        self.mock_st.session_state = {"provider": "OpenAI"}
        self.Utilities.set_api_key_env("sk-test-123")
        self.assertEqual(os.environ.get("OPENAI_API_KEY"), "sk-test-123")

    def test_set_minimax_key(self):
        self.mock_st.session_state = {"provider": "MiniMax"}
        self.Utilities.set_api_key_env("eyJ-minimax-test")
        self.assertEqual(os.environ.get("MINIMAX_API_KEY"), "eyJ-minimax-test")

    def test_default_provider_is_openai(self):
        self.mock_st.session_state = {}
        self.Utilities.set_api_key_env("sk-default")
        self.assertEqual(os.environ.get("OPENAI_API_KEY"), "sk-default")

    def test_minimax_does_not_set_openai_key(self):
        self.mock_st.session_state = {"provider": "MiniMax"}
        os.environ.pop("OPENAI_API_KEY", None)
        self.Utilities.set_api_key_env("eyJ-minimax-test")
        self.assertIsNone(os.environ.get("OPENAI_API_KEY"))


class TestUtilitiesMiniMaxBaseUrl(unittest.TestCase):
    """Test MiniMax base URL constant."""

    def setUp(self):
        self.patcher = patch.dict("sys.modules", _ALL_MOCKS)
        self.patcher.start()
        for mod in ["modules.utils", "modules.chatbot", "modules.embedder"]:
            sys.modules.pop(mod, None)

    def tearDown(self):
        self.patcher.stop()

    def test_minimax_base_url(self):
        from modules.utils import MINIMAX_BASE_URL
        self.assertEqual(MINIMAX_BASE_URL, "https://api.minimax.io/v1")


if __name__ == "__main__":
    unittest.main()
