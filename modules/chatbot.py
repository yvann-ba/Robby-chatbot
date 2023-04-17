import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain


class Chatbot:
    def __init__(self, model_name, temperature, vectors):
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors

    async def conversational_chat(self, query):
        """
        Starts a conversational chat with a model via Langchain
        """

        chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model_name=self.model_name, temperature=self.temperature),
            retriever=self.vectors.as_retriever(),
        )
        result = chain({"question": query, "chat_history": st.session_state["history"]})

        st.session_state["history"].append((query, result["answer"]))

        return result["answer"]
