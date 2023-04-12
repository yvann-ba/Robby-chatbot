import pickle
import streamlit as st
import pandas as pd
import os

from pathlib import Path

from streamlit_chat import message

from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.memory import ChatMessageHistory
from langchain.callbacks import get_openai_callback
import tiktoken
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationalRetrievalChain

# Configure the Streamlit page
st.set_page_config(layout="wide", page_icon="contents\logo_site.png", page_title="Talk-Sheet")

st.markdown(
    "<h1 style='text-align: center;'>Talk-Sheet, Talk with your  sheet-data ! 💬</h1>",
    unsafe_allow_html=True
)

# Input field for the user's OpenAI API key
user_secret = st.sidebar.text_input(
        label="#### Your OpenAI API key 👇",
        placeholder="Paste your openAI API key, sk-",
        type="password",
    )
os.environ["OPENAI_API_KEY"] = user_secret


if user_secret == "":
    st.markdown(
        "<div style='text-align: center;'><h4>Enter your OpenAI API key to start chatting 😉</h4></div>",
        unsafe_allow_html=True
    )
else:
    # Upload CSV file
    uploaded_file = st.sidebar.file_uploader(".", type=["csv"])
    if uploaded_file is not None:
        # Show uploaded CSV file
        def show_user_file(uploaded_file):
            file_container = st.expander("Votre fichier CSV :")
            shows = pd.read_csv(uploaded_file)
            uploaded_file.seek(0)
            file_container.write(shows)
            
        show_user_file(uploaded_file)
        
    else :
        st.sidebar.info(
        
            "👆 Upload a .csv file to get started, "
            "example : [fishfry-locations.csv](https://drive.google.com/file/d/18i7tN2CqrmoouaSqm3hDfAk17hmWx94e/view?usp=sharing)" 
        )
    
    if uploaded_file:
        
        # Save user's CSV file
        def save_user_file(uploaded_file):
            save_folder = 'contents\dataset'
            save_path = Path(save_folder, uploaded_file.name)
            with open(save_path, mode='wb') as w:
                w.write(uploaded_file.getvalue())
                
            file_path_user=os.path.join('contents\dataset', uploaded_file.name)
            return file_path_user
        user_file_path = save_user_file(uploaded_file)
         
        # Create custom prompt for CSV chatbot

        prompt_template = (
        "You are Talk-Sheet, a user-friendly chatbot designed to assist users by engaging in conversations based on data from CSV or Excel files. "
        "Your knowledge comes from:"

        " {context} "

        "Help users by providing relevant information from the data in their files. Answer their questions accurately and concisely. "
        "If the user's specific issue or need cannot be addressed with the available data, "
        "empathize with their situation and suggest that they may need to seek assistance elsewhere. "
        "Always maintain a friendly and helpful tone. "
        "If you don't know the answer to a question, truthfully say you don't know."

        "Human: {question} "

        "Talk-Sheet: "
        )

        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context","question"])

        

        # Create retriever from user's CSV file
        async def store_csv_embeds(file_path_user, filename):
            loader = CSVLoader(file_path=file_path_user, encoding="utf-8")
            data = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
            texts = text_splitter.split_documents(data)

            embeddings = OpenAIEmbeddings()
            
            vectors = Chroma.from_documents(texts, embeddings)
            
            with open(filename + ".pkl", "wb") as f:
                pickle.dump(vectors, f)
        
        async def get_csv_embeds(file_path, filename):
            if not os.path.isfile(filename + ".pkl"):
                await store_csv_embeds(file_path, filename)

            with open(filename + ".pkl", "rb") as f:
                vectors = pickle.load(f)

            return vectors


        async def conversational_chat(query):
            result = qa({"question": query, "chat_history": st.session_state['history']})
            st.session_state['history'].append((query, result["answer"]))
            print("Log: ")
            print(st.session_state['history'])
            return result["answer"]
        
        async def main(): 
            llm = ChatOpenAI(model_name="gpt-3.5-turbo")
            chain = load_qa_chain(llm, chain_type="stuff")
            
            if 'history' not in st.session_state:
                st.session_state['history'] = []
                
            if 'ready' not in st.session_state:
                st.session_state['ready'] = False
                
            # Initialize RetrievalQA with custom prompt and retriever
            qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(model_name="gpt-3.5-turbo"), retriever=retriever_db, return_source_documents=True)
            
            st.session_state['ready'] = True
            
            # Chatbot UI function

            if 'generated' not in st.session_state:
                st.session_state['generated'] = []

            if 'past' not in st.session_state:
                st.session_state['past'] = []
                
            # container for chat history
            response_container = st.container()

            # container for text box
            container = st.container()
            
            with container:
                async def generate_response(query):
                    response = qa.run(query)
                    print(f"Type of response: {type(response)}, response: {response}")
                    return response

                def get_text():
                    input_text = st.text_input("##### Let's Talk ! 👇: ", key="input")
                    return input_text
                
                user_input = get_text()

                if user_input:
                    output = conversational_chat(user_input)

                    st.session_state['past'].append(user_input)
                    st.session_state['generated'].append(output)

            if st.session_state['generated']:
                with response_container:
                    print(f"st.session_state['generated']: {st.session_state['generated']}")
    
                    for i in range(len(st.session_state['generated'])-1, -1, -1):
                        message(st.session_state["generated"][i], key=str(i))
                        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                            





# About section
about = st.sidebar.expander("About Talk-Sheet 🤖")
about.write("#### Talk-Sheet is a user-friendly chatbot designed to assist users by engaging in conversations based on data from CSV or excel files. 📄")
about.write("#### Ideal for various purposes and users, Talk-Sheet provides a simple yet effective way to interact with your sheet-data. 🌐")
about.write("#### Powered by [Langchain]('https://github.com/hwchase17/langchain'), [OpenAI]('https://platform.openai.com/docs/models/gpt-3-5') and [Streamlit]('https://github.com/streamlit/streamlit') Talk-Sheet offers a seamless and personalized experience. ⚡")
