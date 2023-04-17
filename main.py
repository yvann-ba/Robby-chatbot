import os
import streamlit as st
import asyncio
from dotenv import load_dotenv

from streamlit_chat import message

from modules.chatbot import Chatbot
from modules.embedder import Embedder
from modules.history import ChatHistory
from modules.layout import Layout
from modules.sidebar import Sidebar


load_dotenv()

st.set_page_config(layout="wide", page_icon="💬", page_title="ChatBot-PDF")

# Load the OpenAI API key from the .env file or from the user's input
def load_api_key():
    user_api_key = os.getenv("OPENAI_API_KEY")
    if not user_api_key:
        user_api_key = st.sidebar.text_input(
            label="#### Your OpenAI API key 👇", placeholder="Paste your openAI API key, sk-", type="password"
        )
    else:
        st.sidebar.success("API key loaded from .env", icon="🚀")
    return user_api_key


# Handle the file upload and display the uploaded file
def handle_upload():
    uploaded_file = st.sidebar.file_uploader("upload", type="pdf", label_visibility="collapsed")
    if uploaded_file is not None:
        file_container = st.expander("Your PDF file :")
        file_container.write(uploaded_file)
    else:
        st.sidebar.info(
            "👆 Upload your PDF file to get started, "
            "sample for try : [file.pdf](https://github.com/gabacode/chatPDF/blob/main/file.pdf)"
        )
        st.session_state["reset_chat"] = True
    return uploaded_file


# Set up the chatbot with the uploaded file, model, and temperature
async def setup_chatbot(uploaded_file, model, temperature):
    embeds = Embedder()
    with st.spinner("Processing..."):
        uploaded_file.seek(0)
        file = uploaded_file.read()
        vectors = await embeds.getDocEmbeds(file, uploaded_file.name)
        chatbot = Chatbot(model, temperature, vectors)
    st.session_state["ready"] = True
    return chatbot


async def main():

    layout = Layout()
    sidebar = Sidebar()

    layout.display_header()
    user_api_key = load_api_key()

    if user_api_key == "":
        layout.show_api_key_error()
    else:
        os.environ["OPENAI_API_KEY"] = user_api_key
        uploaded_file = handle_upload()

        if uploaded_file is not None:
            history = ChatHistory()
            sidebar.options()
            try:
                chatbot = await setup_chatbot(uploaded_file, st.session_state["model"], st.session_state["temperature"])
                st.session_state["chatbot"] = chatbot

                if st.session_state["ready"]:
                    # Create a containers for displaying the chat history
                    response_container = st.container()
                    container = st.container()

                    with container:
                        with st.form(key="my_form", clear_on_submit=True):
                            user_input = st.text_area(
                                "Query:",
                                placeholder="Ask me anything about the document...",
                                key="input",
                                label_visibility="collapsed",
                            )
                            submit_button = st.form_submit_button(label="Send")

                        if st.session_state["reset_chat"]:
                            history.reset(uploaded_file)

                        history.initialize(uploaded_file)

                        # If the user has submitted a query
                        if submit_button and user_input:
                            history.append("user", user_input)
                            output = await st.session_state["chatbot"].conversational_chat(user_input)
                            history.append("assistant", output)

                    # If there are generated messages to display
                    if st.session_state["assistant"]:
                        with response_container:
                            for i in range(len(st.session_state["assistant"])):
                                message(
                                    st.session_state["user"][i],
                                    is_user=True,
                                    key=f"{i}_user",
                                    avatar_style="big-smile",
                                )
                                message(st.session_state["assistant"][i], key=str(i), avatar_style="thumbs")

            except Exception as e:
                st.error(f"Error: {str(e)}")

    sidebar.about()


# Run the main function using asyncio
if __name__ == "__main__":
    asyncio.run(main())
