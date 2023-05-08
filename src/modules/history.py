import os
import streamlit as st
from streamlit_chat import message

class ChatHistory:
    
    def __init__(self):
        self.history = st.session_state.get("history", [])
        st.session_state["history"] = self.history

    def default_greeting(self):
        return "Hey Robby ! 👋"

    def default_prompt(self, topic):
        return f"Hello ! Ask me anything about {topic} 🤗"

    def initialize_user_history(self):
        st.session_state["user"] = [self.default_greeting()]

    def initialize_assistant_history(self, uploaded_file):
        st.session_state["assistant"] = [self.default_prompt(uploaded_file.name)]

    def initialize(self, uploaded_file):
        if "assistant" not in st.session_state:
            self.initialize_assistant_history(uploaded_file)
        if "user" not in st.session_state:
            self.initialize_user_history()

    def reset(self, uploaded_file):
        st.session_state["history"] = []
        
        self.initialize_user_history()
        self.initialize_assistant_history(uploaded_file)
        st.session_state["reset_chat"] = False

    def append(self, mode, message):
        st.session_state[mode].append(message)

    def generate_messages(self, container):
        if st.session_state["assistant"]:
            with container:
                for i in range(len(st.session_state["assistant"])):
                    message(
                        st.session_state["user"][i],
                        is_user=True,
                        key=f"history_{i}_user",
                        avatar_style="big-smile",
                    )
                    message(st.session_state["assistant"][i], key=str(i), avatar_style="thumbs")

    def load(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                self.history = f.read().splitlines()

    def save(self):
        with open(self.history_file, "w") as f:
            f.write("\n".join(self.history))
