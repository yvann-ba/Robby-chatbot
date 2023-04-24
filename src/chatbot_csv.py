import os
import streamlit as st
from dotenv import load_dotenv
from io import BytesIO
from io import StringIO
import sys
import re
from modules.history import ChatHistory
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar
from langchain.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI

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

            uploaded_file_content = BytesIO(uploaded_file.getvalue())



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
                        
                    if st.session_state["show_csv_agent"]:
                        query = st.text_input(label="Use CSV agent for precise information about the structure of your csv file")
                        if query != "":
                            
                            # Redirigez temporairement la sortie standard vers un objet StringIO
                            old_stdout = sys.stdout
                            sys.stdout = captured_output = StringIO()

                            # Exécutez create_csv_agent et capturez la sortie
                            agent = create_csv_agent(ChatOpenAI(temperature=0), uploaded_file_content, verbose=True, max_iterations=4)

                            # Exécutez la méthode agent.run(query) et capturez la sortie
                            result = agent.run(query)

                            # Restaurez la sortie standard
                            sys.stdout = old_stdout

                            # Récupérez les pensées capturées
                            thoughts = captured_output.getvalue()

                            # Utilisez des expressions régulières pour supprimer les caractères et les séquences indésirables
                            cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)  # Supprime les séquences d'échappement ANSI
                            cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)          # Supprime les parties indésirables comme '[1m>'

                            # Affichez les pensées nettoyées dans un expander
                            with st.expander("Afficher les pensées de l'agent"):
                                st.write(cleaned_thoughts)

                            # Affichez le résultat de create_csv_agent
                            st.write(result)

            except Exception as e:
                st.error(f"Error: {str(e)}")


    sidebar.about()

if __name__ == "__main__":
    main()