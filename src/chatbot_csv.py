import os
import streamlit as st
from dotenv import load_dotenv

from modules.history import ChatHistory
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar

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

            except Exception as e:
                st.error(f"Error: {str(e)}")


    sidebar.about()

if __name__ == "__main__":
    main()