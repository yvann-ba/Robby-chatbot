import os
import pickle
import streamlit as st
import tempfile
import pandas as pd
import asyncio

from streamlit_chat import message
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.prompts.prompt import PromptTemplate


st.set_page_config(layout="wide", page_icon="💬", page_title="ChatBot-CSV")

st.markdown(
    "<h1 style='text-align: center;'>ChatBot-CSV, Talk with your  csv-data ! 💬</h1>",
    unsafe_allow_html=True)

user_api_key = st.sidebar.text_input(
    label="#### Your OpenAI API key 👇",
    placeholder="Paste your openAI API key, sk-",
    type="password")

async def main():
    
    if user_api_key == "":
        
        st.markdown(
            "<div style='text-align: center;'><h4>Enter your OpenAI API key to start chatting 😉</h4></div>",
            unsafe_allow_html=True)
        
    else:
        os.environ["OPENAI_API_KEY"] = user_api_key
        
        uploaded_file = st.sidebar.file_uploader("upload", type="csv", label_visibility="hidden")
        
        if uploaded_file is not None:
            def show_user_file(uploaded_file):
                file_container = st.expander("Your CSV file :")
                shows = pd.read_csv(uploaded_file)
                uploaded_file.seek(0)
                file_container.write(shows)
                
            show_user_file(uploaded_file)
            
        else :
            st.sidebar.info(
            "👆 Upload your CSV file to get started, "
            "sample for try : [fishfry-locations.csv](https://drive.google.com/file/d/18i7tN2CqrmoouaSqm3hDfAk17hmWx94e/view?usp=sharing)" 
            )
    
        if uploaded_file :
            try :
                async def storeDocEmbeds(file, filename):
                    
                    # Write the uploaded file to a temporary file
                    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
                        tmp_file.write(file)
                        tmp_file_path = tmp_file.name

                    # Load the data from the CSV file using Langchain
                    loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8")
                    data = loader.load()

                    embeddings = OpenAIEmbeddings()
                    
                    vectors = FAISS.from_documents(data, embeddings)
                    os.remove(tmp_file_path)

                    with open(filename + ".pkl", "wb") as f:
                        pickle.dump(vectors, f)
                    
                async def getDocEmbeds(file, filename):
                    
                    if not os.path.isfile(filename + ".pkl"):
                        # If not, store the vectors using the storeDocEmbeds function
                        await storeDocEmbeds(file, filename)
                    
                    with open(filename + ".pkl", "rb") as f:
                        #global vectors
                        vectors = pickle.load(f)
                        
                    return vectors

                async def conversational_chat(query):
                    
                    # Use the Langchain ConversationalRetrievalChain to generate a response to the user's query
                    result = chain({"question": query, "chat_history": st.session_state['history']})
                    
                    # Add the user's query and the chatbot's response to the chat history
                    st.session_state['history'].append((query, result["answer"]))
                    
                    # You can print the chat history for debugging :
                    #print("Log: ")
                    #print(st.session_state['history'])
                    
                    return result["answer"]

                # Set up sidebar with various options
                with st.sidebar.expander("🛠️ Settings", expanded=False):
                    
                    # Add a button to reset the chat history
                    if st.button("Reset Chat"):
                        st.session_state['reset_chat'] = True

                    # Allow the user to select a chatbot model to use
                    MODEL = st.selectbox(label='Model', options=['gpt-3.5-turbo','gpt-4'])

                if 'history' not in st.session_state:
                    st.session_state['history'] = []

                if 'ready' not in st.session_state:
                    st.session_state['ready'] = False
                    
                if 'reset_chat' not in st.session_state:
                    st.session_state['reset_chat'] = False
                
                if uploaded_file is not None:

                    # Display a spinner while processing the file
                    with st.spinner("Processing..."):

                        uploaded_file.seek(0)
                        file = uploaded_file.read()
                        
                        # Generate embeddings vectors for the file
                        vectors = await getDocEmbeds(file, uploaded_file.name)

                        _template = """Given the following conversation and a follow-up question, rephrase the follow-up question to be a stand-alone question.
                        You can assume that the question is about the information in a CSV file.
                        Chat History:
                        {chat_history}
                        Follow-up entry: {question}
                        Standalone question:"""
                        CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

                        qa_template = """"You are an AI conversational assistant to answer questions based on information from a csv file.
                        You are given data from a csv file and a question, you must help the user find the information they need. 
                        Only give responses for information you know about. Don't try to make up an answer.
                        Your answers should be short and friendly.
                        Respond to the user in the same language they are speaking to you in.
                        question: {question}
                        =========
                        {context}
                        =======
                        """
                        QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["question", "context"])

                        chain = ConversationalRetrievalChain.from_llm(llm = ChatOpenAI(temperature=0.0,model_name=MODEL),
                                                                      condense_question_prompt=CONDENSE_QUESTION_PROMPT,qa_prompt=QA_PROMPT,retriever=vectors.as_retriever())

                    # Set the "ready" flag to True now that the chatbot is ready to chat
                    st.session_state['ready'] = True

                if st.session_state['ready']:

                    # If the chat history has not yet been initialized, initialize it now
                    if 'generated' not in st.session_state:
                        st.session_state['generated'] = ["Hello ! Ask me anything about " + uploaded_file.name + " 🤗"]

                    if 'past' not in st.session_state:
                        st.session_state['past'] = ["Hey ! 👋"]

                    #container for displaying the chat history
                    response_container = st.container()
                    
                    #container for the user's text input
                    container = st.container()

                    with container:
                        
                        # Create a form for the user to enter their query
                        with st.form(key='my_form', clear_on_submit=True):
                            
                            user_input = st.text_input("Query:", placeholder="Talk about your csv data here (:", key='input')
                            submit_button = st.form_submit_button(label='Send')
                            
                            # If the "reset_chat" flag has been set, reset the chat history and generated messages
                            if st.session_state['reset_chat']:
                                
                                st.session_state['history'] = []
                                st.session_state['past'] = ["Hey ! 👋"]
                                st.session_state['generated'] = ["Hello ! Ask me anything about " + uploaded_file.name + " 🤗"]
                                response_container.empty()
                                st.session_state['reset_chat'] = False

                        if submit_button and user_input:
                            
                            # Generate a response using the Langchain ConversationalRetrievalChain
                            output = await conversational_chat(user_input)
                            
                            # Add the user's input and the chatbot's output to the chat history
                            st.session_state['past'].append(user_input)
                            st.session_state['generated'].append(output)

                    if st.session_state['generated']:
                        
                        # Display the chat history
                        with response_container:
                            
                            for i in range(len(st.session_state['generated'])):
                                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
                

            except Exception as e:
                st.error(f"Error: {str(e)}")

    about = st.sidebar.expander("About 🤖")
    about.write("#### ChatBot-CSV is an AI chatbot featuring conversational memory, designed to enable users to discuss their CSV data in a more intuitive manner. 📄")
    about.write("#### He employs large language models to provide users with seamless, context-aware natural language interactions for a better understanding of their CSV data. 🌐")
    about.write("#### Powered by [Langchain](https://github.com/hwchase17/langchain), [OpenAI](https://platform.openai.com/docs/models/gpt-3-5) and [Streamlit](https://github.com/streamlit/streamlit) ⚡")
    about.write("#### Source code : [yvann-hub/ChatBot-CSV](https://github.com/yvann-hub/ChatBot-CSV)")

#Run the main function using asyncio
if __name__ == "__main__":
    asyncio.run(main())

