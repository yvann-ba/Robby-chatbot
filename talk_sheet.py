
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import pickle
from langchain.document_loaders.csv_loader import CSVLoader


import os
import streamlit as st
from streamlit_chat import message
from langchain.text_splitter import CharacterTextSplitter
import tempfile
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS

import asyncio

 

# vectors = getDocEmbeds("gpt4.pdf")
# qa = ChatVectorDBChain.from_llm(ChatOpenAI(model_name="gpt-3.5-turbo"), vectors, return_source_documents=True)
st.set_page_config(layout="wide", page_icon="contents\logo_site.png", page_title="Talk-Sheet")

st.markdown(
"<h1 style='text-align: center;'>Talk-Sheet, Talk with your  sheet-data ! 💬</h1>",
unsafe_allow_html=True)

user_api_key = st.sidebar.text_input(
    label="#### Your OpenAI API key 👇",
    placeholder="Paste your openAI API key, sk-",
    type="password")

async def main():
    
    if user_api_key == "":
        st.markdown(
            "<div style='text-align: center;'><h4>Enter your OpenAI API key to start chatting 😉</h4></div>",
            unsafe_allow_html=True
        )
    else:
        os.environ["OPENAI_API_KEY"] = user_api_key
        
        uploaded_file = st.sidebar.file_uploader("", type="csv", label_visibility="hidden")
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
    
        
        if uploaded_file :
            async def storeDocEmbeds(file, filename):
                with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
                    tmp_file.write(file)
                    tmp_file_path = tmp_file.name

                loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8")
                data = loader.load()
                
                splitter = CharacterTextSplitter(separator="\n",chunk_size=1500, chunk_overlap=0)
                chunks = splitter.split_documents(data)
                
                embeddings = OpenAIEmbeddings()
                vectors = FAISS.from_documents(chunks, embeddings)
                os.remove(tmp_file_path)

                
                with open(filename + ".pkl", "wb") as f:
                    pickle.dump(vectors, f)

                
            async def getDocEmbeds(file, filename):
                
                if not os.path.isfile(filename + ".pkl"):
                    await storeDocEmbeds(file, filename)
                
                with open(filename + ".pkl", "rb") as f:
                    global vectores
                    vectors = pickle.load(f)
                    
                return vectors

            

            async def conversational_chat(query):
                result = qa({"question": query, "chat_history": st.session_state['history']})
                st.session_state['history'].append((query, result["answer"]))
                print("Log: ")
                print(st.session_state['history'])
                return result["answer"]

            prompt_template = (
            "You are Talk-Sheet, a user-friendly chatbot designed to assist users by engaging in conversations based on data from CSV or Excel files. "
            "Your knowledge comes from:"

            "{context}"

            "Help users by providing relevant information from the data in their files. Answer their questions accurately and concisely. "
            "If the user's specific issue or need cannot be addressed with the available data, "
            "empathize with their situation and suggest that they may need to seek assistance elsewhere. "
            "Always maintain a friendly and helpful tone. "
            "If you don't know the answer to a question, truthfully say you don't know."
            "answers the user's question in the same language as the user"
      
            "Human: {question} "

            "Talk-Sheet: "
            )

            PROMPT = PromptTemplate(template=prompt_template, input_variables=["context","question"])

                    # Set up sidebar with various options
            with st.sidebar.expander("🛠️ setting", expanded=False):
                # Option to preview memory store
                if st.button("Reset Chat"):
                    st.session_state['reset_chat'] = True

                MODEL = st.selectbox(label='Model', options=['gpt-3.5-turbo','gpt-4'])
                
            #llm = ChatOpenAI(model_name="gpt-3.5-turbo")
            #chain = load_qa_chain(llm, chain_type="stuff")
            

            if 'history' not in st.session_state:
                st.session_state['history'] = []


            if 'ready' not in st.session_state:
                st.session_state['ready'] = False
                
            if 'reset_chat' not in st.session_state:
                st.session_state['reset_chat'] = False


            

            if uploaded_file is not None:

                with st.spinner("Processing..."):
                # Add your code here that needs to be executed
                    uploaded_file.seek(0)
                    file = uploaded_file.read()
                    # pdf = PyPDF2.PdfFileReader()
                    vectors = await getDocEmbeds(file, uploaded_file.name)
                    qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(model_name=MODEL), retriever=vectors.as_retriever(), qa_prompt=PROMPT,return_source_documents=False)

                st.session_state['ready'] = True


            if st.session_state['ready']:

                    # Le reste du code existant

                if 'generated' not in st.session_state:
                    st.session_state['generated'] = ["Welcome! You can now ask any questions regarding " + uploaded_file.name]

                if 'past' not in st.session_state:
                    st.session_state['past'] = ["Hey!"]

                # container for chat history
                response_container = st.container()
                
                # container for text box
                container = st.container()

                with container:
                    with st.form(key='my_form', clear_on_submit=True):
                        user_input = st.text_input("Query:", placeholder="e.g: Summarize the paper in a few sentences", key='input')
                        submit_button = st.form_submit_button(label='Send')
                        

                        if st.session_state['reset_chat']:
                            st.session_state['history'] = []
                            st.session_state['past'] = ["Hey!"]
                            st.session_state['generated'] = ["Welcome! You can now ask any questions regarding " + uploaded_file.name]
                            response_container.empty()
                            st.session_state['reset_chat'] = False

                    if submit_button and user_input:
                        output = await conversational_chat(user_input)
                        st.session_state['past'].append(user_input)
                        st.session_state['generated'].append(output)

                if st.session_state['generated']:
                    with response_container:
                        for i in range(len(st.session_state['generated'])):
                            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                            message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
            
    # About section
    about = st.sidebar.expander("About Talk-Sheet 🤖")
    about.write("#### Talk-Sheet is a user-friendly chatbot designed to assist users by engaging in conversations based on data from CSV or excel files. 📄")
    about.write("#### Ideal for various purposes and users, Talk-Sheet provides a simple yet effective way to interact with your sheet-data. 🌐")
    about.write("#### Powered by [Langchain]('https://github.com/hwchase17/langchain'), [OpenAI]('https://platform.openai.com/docs/models/gpt-3-5') and [Streamlit]('https://github.com/streamlit/streamlit') Talk-Sheet offers a seamless and personalized experience. ⚡")

if __name__ == "__main__":
    asyncio.run(main())
