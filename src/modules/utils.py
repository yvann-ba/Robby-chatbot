import os
import pandas as pd
import streamlit as st
import pdfplumber
import pickle
import hashlib

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.vectorstores import FAISS
from modules.chatbot import Chatbot
from modules.embedder import Embedder
from dotenv import find_dotenv, load_dotenv
import logging

load_dotenv(find_dotenv())

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

directory = os.getenv('DOCUMENTS')

class Utilities:
    @staticmethod
    def load_api_key():
        """
        Loads the OpenAI API key from the .env file or 
        from the user's input and returns it
        """
        api_key = st.session_state.get("api_key")

        if os.path.exists(".env") and os.environ.get("OPENAI_API_KEY") is not None:
            user_api_key = os.environ["OPENAI_API_KEY"]
            st.sidebar.success("API key loaded from .env", icon="🚀")
        elif api_key is not None:
            user_api_key = api_key
            st.sidebar.success("API key loaded from previous input", icon="🚀")
        else:
            user_api_key = st.sidebar.text_input(
                label="#### Your OpenAI API key 👇", placeholder="sk-...", type="password"
            )
            if user_api_key:
                st.session_state.api_key = user_api_key

        return user_api_key

    @staticmethod
    def handle_upload(file_types):
        """
        Handles and display uploaded_file
        :param file_types: List of accepted file types, e.g., ["csv", "pdf", "txt"]
        """
        uploaded_file = st.sidebar.file_uploader("upload", type=file_types, label_visibility="collapsed")
        if uploaded_file is not None:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()

            if file_extension== ".pdf" : 
                Utilities.show_pdf_file(uploaded_file)
            elif file_extension== ".txt" : 
                Utilities.show_txt_file(uploaded_file)
        else:
            st.session_state["reset_chat"] = True

        return uploaded_file

    @staticmethod
    def show_pdf_file(uploaded_file):
        file_container = st.expander("Your PDF file :")
        with pdfplumber.open(uploaded_file) as pdf:
            pdf_text = ""
            for page in pdf.pages:
                pdf_text += page.extract_text() + "\n\n"
        file_container.write(pdf_text)

    @staticmethod
    def show_txt_file(uploaded_file):
        file_container = st.expander("Your TXT file:")
        uploaded_file.seek(0)
        content = uploaded_file.read().decode("utf-8")
        file_container.write(content)

    @staticmethod
    def faiss_contexts():
        directory = os.getenv('DATASETS')
        embeddings = OpenAIEmbeddings()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        hash_file_path = "hash.txt"
        
        loader = DirectoryLoader(directory, glob="**/*.txt", show_progress=True)
        documents = loader.load()
        documents_bytes = pickle.dumps(documents)

        hash_object = hashlib.sha256(documents_bytes)
        hex_dig = hash_object.hexdigest()

        old_hash = None
        if os.path.exists(hash_file_path):
            with open(hash_file_path, "r") as f:
                old_hash = f.read().strip()

        if old_hash is None or old_hash != hex_dig:
            with open(hash_file_path, "w") as f:
                f.write(hex_dig)
            documents = text_splitter.split_documents(documents)
            db = FAISS.from_documents(documents, embeddings)
            
            # Save FAISS index
            with open('faiss_index.pkl', 'wb') as f:
                pickle.dump(db, f)
            return db
        else:
            # If the hash hasn't changed, load the 'db' object from the 'faiss_index.pkl' file
            with open('faiss_index.pkl', 'rb') as f:
                db = pickle.load(f)
            return db

    @staticmethod
    def setup_chatbot_with_faiss(model, temperature):
        """
        Sets up the chatbot with the uploaded file, model, and temperature
        """
        with st.spinner("Processing..."):
            vectors = Utilities.faiss_contexts()

            # Create a Chatbot instance with the specified model and temperature
            chatbot = Chatbot(model, temperature, vectors)
        st.session_state["ready"] = True

        return chatbot
    
    @staticmethod
    def setup_chatbot_with_file(uploaded_file, model, temperature):
        """
        Sets up the chatbot with the uploaded file, model, and temperature
        """
        embeds = Embedder()

        with st.spinner("Processing..."):
            uploaded_file.seek(0)
            file = uploaded_file.read()
            # Get the document embeddings for the uploaded file
            vectors = embeds.getDocEmbeds(file, uploaded_file.name)

            # Create a Chatbot instance with the specified model and temperature
            chatbot = Chatbot(model, temperature, vectors)
        st.session_state["ready"] = True

        return chatbot
