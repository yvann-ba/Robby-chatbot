from modules.tabulars_tools import handle_csv_agent, handle_pandas_ai 
import os
import streamlit as st
from dotenv import load_dotenv

from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar

st.set_page_config(layout="wide", page_icon="💬", page_title="Robby | Chat-Bot 🤖")
load_dotenv()

layout, sidebar, utils = Layout(), Sidebar(), Utilities()

layout.show_header("CSV")

user_api_key = utils.load_api_key()
os.environ["OPENAI_API_KEY"] = user_api_key
if not user_api_key:
    layout.show_api_key_missing()
else:


    uploaded_file = utils.handle_upload(["csv"])

    if uploaded_file:
        # Configure the sidebar
        sidebar.show_options()

        handle_csv_agent(uploaded_file)

        handle_pandas_ai(uploaded_file)

sidebar.about()