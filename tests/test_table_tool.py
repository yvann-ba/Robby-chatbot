"""Unit tests for PandasAgent multi-provider support."""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


class TestPandasAgentProvider(unittest.TestCase):
    """Test PandasAgent provider selection."""

    def _import_pandas_agent(self, provider, api_key_env=None):
        """Import PandasAgent with mocked dependencies and given provider."""
        mock_st = MagicMock()
        mock_st.session_state = {"provider": provider}

        mock_litellm_cls = MagicMock()
        mock_pai = MagicMock()
        mock_pai_config = MagicMock()
        mock_pai.config = mock_pai_config

        mocks = {
            "streamlit": mock_st,
            "matplotlib": MagicMock(),
            "matplotlib.pyplot": MagicMock(),
            "pandasai": mock_pai,
            "pandasai_litellm": MagicMock(LiteLLM=mock_litellm_cls),
            "langchain_community": MagicMock(),
            "langchain_community.callbacks": MagicMock(),
        }

        if api_key_env:
            for k, v in api_key_env.items():
                os.environ[k] = v

        with patch.dict("sys.modules", mocks):
            for m in ["modules.robby_sheet.table_tool", "modules.robby_sheet"]:
                sys.modules.pop(m, None)
            from modules.robby_sheet.table_tool import PandasAgent
            agent = PandasAgent()

        if api_key_env:
            for k in api_key_env:
                os.environ.pop(k, None)

        return agent, mock_litellm_cls, mock_pai_config

    def test_openai_provider_model(self):
        _, mock_litellm, _ = self._import_pandas_agent(
            "OpenAI", {"OPENAI_API_KEY": "sk-test"}
        )
        call_kwargs = mock_litellm.call_args[1]
        self.assertEqual(call_kwargs["model"], "openai/gpt-4o-mini")

    def test_minimax_provider_model(self):
        _, mock_litellm, _ = self._import_pandas_agent(
            "MiniMax", {"MINIMAX_API_KEY": "eyJ-test"}
        )
        call_kwargs = mock_litellm.call_args[1]
        self.assertEqual(call_kwargs["model"], "openai/MiniMax-M2.7")
        self.assertEqual(call_kwargs["api_base"], "https://api.minimax.io/v1")

    def test_minimax_uses_minimax_api_key(self):
        _, mock_litellm, _ = self._import_pandas_agent(
            "MiniMax", {"MINIMAX_API_KEY": "eyJ-key-123"}
        )
        call_kwargs = mock_litellm.call_args[1]
        self.assertEqual(call_kwargs["api_key"], "eyJ-key-123")

    def test_pai_config_set_called(self):
        _, _, mock_config = self._import_pandas_agent(
            "OpenAI", {"OPENAI_API_KEY": "sk-test"}
        )
        mock_config.set.assert_called_once()


if __name__ == "__main__":
    unittest.main()
