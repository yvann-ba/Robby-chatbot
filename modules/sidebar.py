import streamlit as st


class Sidebar:
    MODEL_OPTIONS = ["gpt-3.5-turbo"]
    TEMPERATURE_MIN_VALUE = 0.0
    TEMPERATURE_MAX_VALUE = 1.0
    TEMPERATURE_DEFAULT_VALUE = 0.618
    TEMPERATURE_STEP = 0.01

    def __init__(self):
        pass

    def about(self):
        about = st.sidebar.expander("About 🤖")
        sections = [
            "#### ChatBot-PDF is an AI chatbot featuring conversational memory, designed to enable users to discuss their PDF data in a more intuitive manner. 📄",
            "#### This is a fork of [ChatBot-CSV](https://github.com/yvann-hub/ChatBot-CSV) by [yvann-hub](https://github.com/yvann-hub), many thanks to him for his work. 🤗",
            "#### It employs large language models to provide users with seamless, context-aware natural language interactions for a better understanding of their data. 🌐",
            "#### Powered by [Langchain](https://github.com/hwchase17/langchain), [OpenAI](https://platform.openai.com/docs/models/gpt-3-5) and [Streamlit](https://github.com/streamlit/streamlit) ⚡",
            "#### Source code : [gabacode/ChatBot-PDF](https://github.com/gabacode/ChatBot-PDF)",
        ]
        for section in sections:
            about.write(section)

    def reset_chat_button(self):
        if st.button("Reset chat"):
            st.session_state["reset_chat"] = True
        st.session_state.setdefault("reset_chat", False)

    def model_selector(self):
        model = st.selectbox(label="Model", options=self.MODEL_OPTIONS)
        st.session_state["model"] = model

    def temperature_slider(self):
        temperature = st.slider(
            label="Temperature",
            min_value=self.TEMPERATURE_MIN_VALUE,
            max_value=self.TEMPERATURE_MAX_VALUE,
            value=self.TEMPERATURE_DEFAULT_VALUE,
            step=self.TEMPERATURE_STEP,
        )
        st.session_state["temperature"] = temperature

    def options(self):
        with st.sidebar.expander("🛠️ Settings", expanded=False):
            self.reset_chat_button()
            self.model_selector()
            self.temperature_slider()
            st.session_state.setdefault("model", self.MODEL_OPTIONS[0])
            st.session_state.setdefault("temperature", self.TEMPERATURE_DEFAULT_VALUE)
