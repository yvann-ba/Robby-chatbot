
import re
import sys
from io import StringIO, BytesIO
import matplotlib.pyplot as plt
import streamlit as st
from langchain.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from streamlit_chat import message

import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI



class CsvAgent :

    @staticmethod
    def count_tokens_agent(agent, query):
        """
        Count the tokens used by the CSV Agent
        """
        with get_openai_callback() as cb:
            result = agent(query)
            st.write(f'Spent a total of {cb.total_tokens} tokens')

        return result
    
    def __init__(self, uploaded_file_content):
        self.agent = self.create_agent(uploaded_file_content)

    def create_agent(self, uploaded_file_content):
        llm=ChatOpenAI(temperature=st.session_state["temperature"],
                       model_name=st.session_state["model"],request_timeout=120
                       )
        return create_pandas_dataframe_agent(llm=llm,
                                df = uploaded_file_content,
                                verbose=True, max_iterations=5
                                )

    def get_agent_response(self, query):
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        result = self.agent.run(query)
        sys.stdout = old_stdout
        return result, captured_output

    def process_agent_thoughts(self,captured_output):
        thoughts = captured_output.getvalue()
        cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
        cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)
        return cleaned_thoughts

    def display_agent_thoughts(self,cleaned_thoughts):
        with st.expander("Display the agent's thoughts"):
            st.write(cleaned_thoughts)

    def update_chat_history(self,query, result):
        st.session_state.chat_history.append(("user", query))
        st.session_state.chat_history.append(("agent", result))

    def display_chat_history(self):
        for i, (sender, message_text) in enumerate(st.session_state.chat_history):
            if sender == "user":
                message(message_text, is_user=True, key=f"{i}_user")
            else:
                message(message_text, key=f"{i}")


def handle_pandas_ai(uploaded_file):
    if "show_pandas_ai" not in st.session_state:
        st.session_state["show_pandas_ai"] = False

    if st.button("Pandas AI"):
        st.session_state["show_pandas_ai"] = not st.session_state["show_pandas_ai"]
    if st.session_state["show_pandas_ai"]:

        uploaded_file_content = BytesIO(uploaded_file.getvalue())
        df = pd.read_csv(uploaded_file_content)

        st.session_state.df = df
        with st.form(key="Question"):

                question = st.text_input("Ask PandasAI (experimental), Type Plot at the beginning of your query for make graph", value="", type="default", 
                    placeholder="e-g : Plot the histogram of countries showing for each the gpd, using different colors for each bar "
                    )

                submitted = st.form_submit_button("Submit")
                if submitted:
                    with st.spinner():
                        llm = OpenAI()

                        pandas_ai = PandasAI(llm, verbose=True, enforce_privacy=True)

                        response = pandas_ai.run(df, prompt=question)
                        fig = plt.gcf()
                        if fig.get_axes():
                            st.pyplot(fig)
                        st.write(response)

        if st.session_state.df is not None:
            st.subheader("Current dataframe:")
            st.write(st.session_state.df)
