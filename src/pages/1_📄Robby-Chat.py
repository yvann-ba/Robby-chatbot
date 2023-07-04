import os
import streamlit as st
from io import StringIO
import re
import sys
from modules.history import ChatHistory
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Function to reload module for local development
def reload_module(module_name):
    import importlib
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    return sys.modules[module_name]

# Reload modules
history_module = reload_module('modules.history')
layout_module = reload_module('modules.layout')
utils_module = reload_module('modules.utils')
sidebar_module = reload_module('modules.sidebar')

# Assign reloaded modules to variables
ChatHistory = history_module.ChatHistory
Layout = layout_module.Layout
Utilities = utils_module.Utilities
Sidebar = sidebar_module.Sidebar

# Set page config
st.set_page_config(layout="wide", page_icon="💬", page_title="Isabella | Wedding Chatbot 👰🏽🤵🏻‍♂️💍🤖")

# Instantiate main components
layout, sidebar, utils = Layout(), Sidebar(), Utilities()

# Show header
layout.show_header("PDF, TXT, CSV")

# Load API key
user_api_key = utils.load_api_key()

# Check if API key is present
if not user_api_key:
    layout.show_api_key_missing()
else:
    os.environ["OPENAI_API_KEY"] = user_api_key
    
    # Configure sidebar
    sidebar.show_options()
    sidebar.about()
    
    # Initialize chat history
    history = ChatHistory()
    try:
        # Setup chatbot with faiss
        chatbot = utils.setup_chatbot_with_faiss(
            st.session_state["model"],
            st.session_state["temperature"]
        )
        st.session_state["chatbot"] = chatbot
        logging.info('Chatbot setup successful')

        if st.session_state["ready"]:
            # Create containers for chat responses and user prompts
            response_container, prompt_container = st.container(), st.container()

            with prompt_container:
                # Display prompt form
                is_ready, user_input_container = layout.prompt_form()

                # Initialize chat history
                history.initialize()
                logging.debug('Chat history initialized')

                # Reset chat history if button clicked
                if st.session_state["reset_chat"]:
                    history.reset()
                    logging.info('Chat history reset')

                if is_ready:
                    # Update chat history and display chat messages
                    history.append("user", user_input_container)

                    old_stdout = sys.stdout
                    sys.stdout = captured_output = StringIO()

                    output = st.session_state["chatbot"].conversational_chat(user_input_container)

                    sys.stdout = old_stdout

                    history.append("assistant", output)
                    logging.debug('Chat history updated')

                    # Clean up agent's thoughts to remove unwanted characters
                    thoughts = captured_output.getvalue()
                    cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
                    cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)

                    # Display agent's thoughts
                    with st.expander("Display the agent's thoughts"):
                        st.write(cleaned_thoughts)

            # Generate chat messages
            history.generate_messages(response_container)
            logging.info('Chat messages generated')
    except Exception as e:
        st.error(f"Error: {str(e)}")
        logging.error(f"Error: {str(e)}")