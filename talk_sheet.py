from fastapi import Query
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
from langchain.callbacks import get_openai_callback
from sympy import use
import tiktoken
from langchain.chains import ConversationChain
from langchain.memory import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains import LLMChain
from langchain.chains.conversation.memory import ConversationSummaryMemory




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
    uploaded_file = st.sidebar.file_uploader(label=" ",label_visibility='hidden', type=["csv"])
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
        save_folder = 'contents\dataset'
        save_path = Path(save_folder, uploaded_file.name)
        with open(save_path, mode='wb') as w:
            w.write(uploaded_file.getvalue())
            
        file_path_user=os.path.join('contents\dataset', uploaded_file.name)

        memory = ConversationSummaryMemory(llm=OpenAI(), memory_key="chat_history")
        

        with st.sidebar.expander(" 🛠️ Settings ", expanded=False):

            MODEL = st.selectbox(label='Model', options=['gpt-3.5-turbo','gpt-4'])
            

        try:
            # Create retriever from user's CSV file
            loader = CSVLoader(file_path=file_path_user, encoding="utf-8")
            data = loader.load()
            text_splitter = CharacterTextSplitter(separator="\n",chunk_size=1500, chunk_overlap=0)
            documents = text_splitter.split_documents(data)

            embeddings = OpenAIEmbeddings()
            
            vectorstore = Chroma.from_documents(documents, embeddings)

            # return ConversationRetrievalChain that answers user questions based on a given document store
            chain = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0, model_name=MODEL),
                retriever=vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":2})
            )
    
            # Chatbot UI function
            if 'generated' not in st.session_state:
                st.session_state['generated'] = []

            if 'past' not in st.session_state:
                st.session_state['past'] = []

            def generate_response(query):
                chat_history = []

                result = chain({'chat_history': {}, 'question': query})
                chat_history = []
                query = query
                result = chain({"question": query, "chat_history": chat_history})
                response = result["answer"]
                print(f"Type of response: {type(response)}, response: {response}")
                return response

            def get_text():
                input_text = st.text_input("##### Let's Talk ! 👇: ", key="input", placeholder="Your AI assistant here! Ask me anything ...")
                return input_text
            
            user_input = get_text()

            if user_input:
                output = generate_response(user_input)

                st.session_state.past.append(user_input)
                st.session_state.generated.append(output)

            if st.session_state['generated']:
                print(f"st.session_state['generated']: {st.session_state['generated']}")

                for i in range(len(st.session_state['generated'])-1, -1, -1):
                    message(st.session_state["generated"][i], key=str(i))
                    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        except Exception as e:
            st.error(f"Error: {str(e)}")



# About section
about = st.sidebar.expander("About Talk-Sheet 🤖")
about.write("#### Talk-Sheet is a user-friendly chatbot designed to assist users by engaging in conversations based on data from CSV or excel files. 📄")
about.write("#### Ideal for various purposes and users, Talk-Sheet provides a simple yet effective way to interact with your sheet-data. 🌐")
about.write("#### Powered by [Langchain]('https://github.com/hwchase17/langchain'), [OpenAI]('https://platform.openai.com/docs/models/gpt-3-5') and [Streamlit]('https://github.com/streamlit/streamlit') Talk-Sheet offers a seamless and personalized experience. ⚡")
