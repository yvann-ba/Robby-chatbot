from langchain.agents import create_csv_agent
import streamlit as st

from langchain.llms import OpenAI


def extra_chatbot_page():

    query = st.text_input(label="Use CSV agent for precise informations about the csv file itself")

    if query :
        agent = create_csv_agent(OpenAI(temperature=0), 'poto-associations-sample.csv', verbose=True)
        if agent :
            st.write(agent.run(query))

if __name__ == "__main__":
    extra_chatbot_page()


