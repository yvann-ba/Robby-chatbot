import os
import importlib
import sys
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from io import StringIO, BytesIO
from modules.robby_sheet.table_tool import CsvAgent, handle_pandas_ai
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar

def reload_module(module_name):
    """For update changes
    made to modules in localhost (press r)"""

    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    return sys.modules[module_name]

table_tool_module = reload_module('modules.robby_sheet.table_tool')
layout_module = reload_module('modules.layout')
utils_module = reload_module('modules.utils')
sidebar_module = reload_module('modules.sidebar')


st.set_page_config(layout="wide", page_icon="💬", page_title="Robby | Chat-Bot 🤖")

layout, sidebar, utils = Layout(), Sidebar(), Utilities()

layout.show_header("CSV")

user_api_key = utils.load_api_key()
os.environ["OPENAI_API_KEY"] = user_api_key


if not user_api_key:
    layout.show_api_key_missing()

else:

    uploaded_file = utils.handle_upload(["csv"])

    if uploaded_file:

        sidebar.show_options()

        uploaded_file_content = BytesIO(uploaded_file.getvalue())
        df = pd.read_csv(uploaded_file_content)
        
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
        csv_agent = CsvAgent(df)
        query = st.text_input("Ask CSV Agent :", value="", type="default",  placeholder="e-g : How many rows in my file ?")

        if query :
            result, captured_output = csv_agent.get_agent_response(query)
            cleaned_thoughts = csv_agent.process_agent_thoughts(captured_output)
            csv_agent.display_agent_thoughts(cleaned_thoughts)
            csv_agent.update_chat_history(query, result)
            csv_agent.display_chat_history()


        handle_pandas_ai(uploaded_file)

sidebar.about()