import os
import streamlit as st
from dotenv import load_dotenv
from io import BytesIO
from io import StringIO
import sys
import re
from langchain.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI
from modules.history import ChatHistory
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar
from modules.chatbot import Chatbot

#To be able to update the changes made to modules in localhost,
#you can press the "r" key on the localhost page to refresh and reflect the changes made to the module files.
def reload_module(module_name):
    import importlib
    import sys
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    return sys.modules[module_name]

chatbot_module = reload_module('modules.chatbot')
history_module = reload_module('modules.history')
layout_module = reload_module('modules.layout')
utils_module = reload_module('modules.utils')
sidebar_module = reload_module('modules.sidebar')

Chatbot = chatbot_module.Chatbot
ChatHistory = history_module.ChatHistory
Layout = layout_module.Layout
Utilities = utils_module.Utilities
Sidebar = sidebar_module.Sidebar


def init():
    load_dotenv()
    st.set_page_config(layout="wide", page_icon="💬", page_title="ChatBot-CSV")

def main():

    init()
    layout, sidebar, utils = Layout(), Sidebar(), Utilities()
    layout.show_header()
    user_api_key = utils.load_api_key()

    if not user_api_key:
        layout.show_api_key_missing()
    else:
        os.environ["OPENAI_API_KEY"] = user_api_key
        uploaded_file = utils.handle_upload()

        if uploaded_file:
            history = ChatHistory()
            sidebar.show_options()


            try:
                chatbot = utils.setup_chatbot(
                    uploaded_file, st.session_state["model"], st.session_state["temperature"]
                )
                st.session_state["chatbot"] = chatbot

                if st.session_state["ready"]:
                    response_container, prompt_container = st.container(), st.container()

                    with prompt_container:
                        is_ready, user_input = layout.prompt_form()

                        history.initialize(uploaded_file)
                        if st.session_state["reset_chat"]:
                            history.reset(uploaded_file)

                        if is_ready:
                            history.append("user", user_input)
                            output = st.session_state["chatbot"].conversational_chat(user_input)
                            history.append("assistant", output)
                    history.generate_messages(response_container)

                    #CSV Agent part
                    if st.session_state["show_csv_agent"]:
                        query = st.text_input(label="Use CSV agent for precise information about the structure of your csv file", placeholder="ex : how many rows in my file ?")
                        if query != "":
                            uploaded_file_content = BytesIO(uploaded_file.getvalue())

                            old_stdout = sys.stdout
                            sys.stdout = captured_output = StringIO()
                            agent = create_csv_agent(ChatOpenAI(temperature=0), uploaded_file_content, verbose=True, max_iterations=4)

                            result = agent.run(query)

                            sys.stdout = old_stdout
                            thoughts = captured_output.getvalue()

                            cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
                            cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)

                            with st.expander("Display the agent's thoughts"):
                                st.write(cleaned_thoughts)
                                
                                Utilities.count_tokens_agent(agent, query) #count and print numbers of tokens used

                            st.write(result)

            except Exception as e:
                st.error(f"Error: {str(e)}")

    sidebar.about()

if __name__ == "__main__":
    main()