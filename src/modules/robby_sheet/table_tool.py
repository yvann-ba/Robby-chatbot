import re
import sys
from io import StringIO, BytesIO
import matplotlib.pyplot as plt
import streamlit as st
from langchain_community.callbacks import get_openai_callback
import pandasai as pai
from pandasai_litellm import LiteLLM
import os

class PandasAgent:

    def __init__(self):
        # Configure PandasAI with OpenAI via LiteLLM
        api_key = os.environ.get("OPENAI_API_KEY", "")
        llm = LiteLLM(model="openai/gpt-4o-mini", api_key=api_key)
        pai.config.set({"llm": llm})

    @staticmethod
    def count_tokens_agent(agent, query):
        """
        Count the tokens used by the CSV Agent
        """
        with get_openai_callback() as cb:
            result = agent(query)
            st.write(f'Spent a total of {cb.total_tokens} tokens')
        return result

    def get_agent_response(self, df, query):
        """
        Get response from PandasAI v3
        """
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            # Create PandasAI DataFrame and chat
            df_pai = pai.DataFrame(df)
            response = df_pai.chat(query)
            
            # Check for generated plots
            fig = plt.gcf()
            if fig.get_axes():
                fig.set_size_inches(12, 6)
                plt.tight_layout()
                buf = BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)
                st.image(buf, caption="Generated Plot")
                plt.clf()  # Clear the figure
        except Exception as e:
            response = f"Error: {str(e)}"
        
        sys.stdout = old_stdout
        return response, captured_output

    def process_agent_thoughts(self, captured_output):
        thoughts = captured_output.getvalue()
        cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
        cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)
        return cleaned_thoughts

    def display_agent_thoughts(self, cleaned_thoughts):
        with st.expander("Display the agent's thoughts"):
            st.write(cleaned_thoughts)

    def update_chat_history(self, query, result):
        st.session_state.chat_history.append(("user", query))
        st.session_state.chat_history.append(("agent", result))

    def display_chat_history(self):
        """
        Display chat history using native Streamlit chat elements
        """
        for i, (sender, message_text) in enumerate(st.session_state.chat_history):
            if sender == "user":
                with st.chat_message("user", avatar="😊"):
                    st.write(message_text)
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(message_text)