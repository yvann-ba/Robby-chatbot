import os
import streamlit as st
from io import StringIO
import re
import sys
from modules.history import ChatHistory
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar
from io import BytesIO
import pandas as pd

#To be able to update the changes made to modules in localhost (press r)
def reload_module(module_name):
    import importlib
    import sys
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    return sys.modules[module_name]

history_module = reload_module('modules.history')
layout_module = reload_module('modules.layout')
utils_module = reload_module('modules.utils')
sidebar_module = reload_module('modules.sidebar')

ChatHistory = history_module.ChatHistory
Layout = layout_module.Layout
Utilities = utils_module.Utilities
Sidebar = sidebar_module.Sidebar

st.set_page_config(layout="wide", page_icon="💬", page_title="Bob | Chat-Bot 🤖")

# Instantiate the main components
layout, sidebar, utils = Layout(), Sidebar(), Utilities()

layout.show_header("PDF, TXT, CSV")

user_api_key = utils.load_api_key()

if not user_api_key:
    layout.show_api_key_missing()
else:
    os.environ["OPENAI_API_KEY"] = user_api_key

    prod_uploaded_file = utils.handle_upload(["pdf", "txt", "csv"], key="prod")
    dev_uploaded_file = utils.handle_upload(["pdf", "txt", "csv"], key="dev")

    if prod_uploaded_file and dev_uploaded_file:

        # Query
        prod_file_content = BytesIO(prod_uploaded_file.getvalue())
        dev_file_content = BytesIO(dev_uploaded_file.getvalue())

        df_prod = pd.read_csv(prod_file_content).to_json(orient='records')

        df_dev = pd.read_csv(dev_file_content).to_json(orient='records')

        # Configure the sidebar
        sidebar.show_options()
        sidebar.about()

        # Initialize chat history
        history = ChatHistory()
        try:
            chatbot = utils.setup_chatbot(
                prod_uploaded_file, st.session_state["model"], st.session_state["temperature"],
                df_prod, df_dev
            )
            st.session_state["chatbot"] = chatbot

            if st.session_state["ready"]:
                # Create containers for chat responses and user prompts
                response_container, prompt_container = st.container(), st.container()

                with prompt_container:
                    # Display the prompt form
                    is_ready, user_input = layout.prompt_form()

                    # Initialize the chat history
                    history.initialize()

                    # Reset the chat history if button clicked
                    if st.session_state["reset_chat"]:
                        history.reset()

                    if is_ready:
                        # Update the chat history and display the chat messages
                        history.append("user", user_input)

                        old_stdout = sys.stdout
                        sys.stdout = captured_output = StringIO()

                        output = st.session_state["chatbot"].conversational_chat(user_input,  df_prod=df_prod,df_dev=df_dev,)

                        sys.stdout = old_stdout

                        history.append("assistant", output)

                        # Clean up the agent's thoughts to remove unwanted characters
                        thoughts = captured_output.getvalue()
                        cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
                        cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)

                        # Display the agent's thoughts
                        with st.expander("Display the agent's thoughts"):
                            st.write(cleaned_thoughts)

                history.generate_messages(response_container)
        except Exception as e:
            st.error(f"Error: {str(e)}")


