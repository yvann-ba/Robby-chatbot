import streamlit as st
from qa_associations import qa_associations

# streamlit run src/app.py

# Configure the Streamlit page
st.set_page_config(layout="wide", page_icon="assets/logo_poto.png", page_title="MonAmiPoto")

# Render the main header
st.markdown(
    "<h1 style='text-align: center;'>Mon Ami Poto, l'ami virtuel qui vous veut du bien ! 💛</h1>",
    unsafe_allow_html=True
)

# Input field for the user's OpenAI API key
user_secret = st.sidebar.text_input(
        label="#### Your OpenAI API key 👇",
        placeholder="Paste your openAI API key, sk-",
        type="password",
    )

# Call the main function with the provided API key
qa_associations(user_secret)