import streamlit as st

class Sidebar:

    PROVIDER_OPTIONS = ["OpenAI", "MiniMax"]

    PROVIDER_MODELS = {
        "OpenAI": ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        "MiniMax": ["MiniMax-M2.7", "MiniMax-M2.7-highspeed"],
    }

    TEMPERATURE_MIN_VALUE = 0.0
    TEMPERATURE_MAX_VALUE = 1.0
    TEMPERATURE_DEFAULT_VALUE = 0.0
    TEMPERATURE_STEP = 0.01

    @staticmethod
    def about():
        about = st.sidebar.expander("🧠 About Robby ")
        sections = [
            "#### Robby is an AI chatbot with a conversational memory, designed to allow users to discuss their data in a more intuitive way. 📄",
            "#### It uses large language models to provide users with natural language interactions about user data content. 🌐",
            "#### Powered by [Langchain](https://github.com/langchain-ai/langchain), [OpenAI](https://platform.openai.com/docs/models), [MiniMax](https://www.minimax.io/) and [Streamlit](https://github.com/streamlit/streamlit) ⚡",
            "#### Source code: [yvann-hub/Robby-chatbot](https://github.com/yvann-hub/Robby-chatbot)",
        ]
        for section in sections:
            about.write(section)

    @staticmethod
    def reset_chat_button():
        if st.button("Reset chat"):
            st.session_state["reset_chat"] = True
        st.session_state.setdefault("reset_chat", False)

    def provider_selector(self):
        provider = st.selectbox(label="Provider", options=self.PROVIDER_OPTIONS)
        st.session_state["provider"] = provider

    def model_selector(self):
        provider = st.session_state.get("provider", "OpenAI")
        model_options = self.PROVIDER_MODELS.get(provider, self.PROVIDER_MODELS["OpenAI"])
        model = st.selectbox(label="Model", options=model_options)
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

    def show_options(self):
        with st.sidebar.expander("🛠️ Robby's Tools", expanded=False):

            self.reset_chat_button()
            self.provider_selector()
            self.model_selector()
            self.temperature_slider()
            st.session_state.setdefault("provider", self.PROVIDER_OPTIONS[0])
            st.session_state.setdefault("model", self.PROVIDER_MODELS["OpenAI"][0])
            st.session_state.setdefault("temperature", self.TEMPERATURE_DEFAULT_VALUE)