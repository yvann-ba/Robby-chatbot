import streamlit as st
from chat_csv import chat_csv

# streamlit run src/app.py

# Configure the Streamlit page
st.set_page_config(layout="wide", page_icon="contents\logo_site.png", page_title="Talk-Sheet")

# Render the main header
st.markdown(
    "<h1 style='text-align: center;'>Talk-Sheet, Talk with your  sheet-data ! 💬</h1>",
    unsafe_allow_html=True
)

# Input field for the user's OpenAI API key
user_secret = st.sidebar.text_input(
        label="#### Your OpenAI API key 👇",
        placeholder="Paste your openAI API key, sk-",
        type="password",
    )

# Call the main function with the provided API key
chat_csv(user_secret)