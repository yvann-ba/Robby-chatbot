import os
import pickle
import streamlit as st
import tempfile
import pandas as pd
import asyncio

# Import modules needed for building the chatbot application
from streamlit_chat import message
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS

# Set the Streamlit page configuration, including the layout and page title/icon
st.set_page_config(layout="wide", page_icon="💬", page_title="ChatBot-CSV")

# Display the header for the application using HTML markdown
st.markdown(
    "<h1 style='text-align: center;'>ChatBot-CSV, Talk with your  csv-data ! 💬</h1>",
    unsafe_allow_html=True)

# Allow the user to enter their OpenAI API key
user_api_key = st.sidebar.text_input(
    label="#### Your OpenAI API key 👇",
    placeholder="Paste your openAI API key, sk-",
    type="password")

async def main():
    
    # Check if the user has entered an OpenAI API key
    if user_api_key == "":
        
        # Display a message asking the user to enter their API key
        st.markdown(
            "<div style='text-align: center;'><h4>Enter your OpenAI API key to start chatting 😉</h4></div>",
            unsafe_allow_html=True)
        
    else:
        # Set the OpenAI API key as an environment variable
        os.environ["OPENAI_API_KEY"] = user_api_key
        
        # Allow the user to upload a CSV file
        uploaded_file = st.sidebar.file_uploader("upload", type="csv", label_visibility="hidden")
        
        # If the user has uploaded a file, display it in an expander
        if uploaded_file is not None:
            def show_user_file(uploaded_file):
                file_container = st.expander("Your CSV file :")
                shows = pd.read_csv(uploaded_file)
                uploaded_file.seek(0)
                file_container.write(shows)
                
            show_user_file(uploaded_file)
            
        # If the user has not uploaded a file, display a message asking them to do so
        else :
            st.sidebar.info(
            "👆 Upload your CSV file to get started, "
            "sample for try : [fishfry-locations.csv](https://drive.google.com/file/d/18i7tN2CqrmoouaSqm3hDfAk17hmWx94e/view?usp=sharing)" 
            )
    
        if uploaded_file :
            try :
                # Define an asynchronous function for storing document embeddings using Langchain and FAISS
                async def storeDocEmbeds(file, filename):
                    
                    # Write the uploaded file to a temporary file
                    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
                        tmp_file.write(file)
                        tmp_file_path = tmp_file.name

                    # Load the data from the CSV file using Langchain
                    loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8")
                    data = loader.load()

                    # Create an embeddings object using Langchain
                    embeddings = OpenAIEmbeddings()
                    
                    # Store the embeddings vectors using FAISS
                    vectors = FAISS.from_documents(data, embeddings)
                    os.remove(tmp_file_path)

                    # Save the vectors to a pickle file
                    with open(filename + ".pkl", "wb") as f:
                        pickle.dump(vectors, f)
                    
                # Define an asynchronous function for retrieving document embeddings
                async def getDocEmbeds(file, filename):
                    
                    # Check if embeddings vectors have already been stored in a pickle file
                    if not os.path.isfile(filename + ".pkl"):
                        # If not, store the vectors using the storeDocEmbeds function
                        await storeDocEmbeds(file, filename)
                    
                    # Load the vectors from the pickle file
                    with open(filename + ".pkl", "rb") as f:
                        #global vectors
                        vectors = pickle.load(f)
                        
                    return vectors

                # Define an asynchronous function for conducting conversational chat using Langchain
                async def conversational_chat(query):
                    
                    # Use the Langchain ConversationalRetrievalChain to generate a response to the user's query
                    result = chain({"question": query, "chat_history": st.session_state['history']})
                    
                    # Add the user's query and the chatbot's response to the chat history
                    st.session_state['history'].append((query, result["answer"]))
                    
                    # Print the chat history for debugging purposes
                    print("Log: ")
                    print(st.session_state['history'])
                    
                    return result["answer"]

                # Set up sidebar with various options
                with st.sidebar.expander("🛠️ Settings", expanded=False):
                    
                    # Add a button to reset the chat history
                    if st.button("Reset Chat"):
                        st.session_state['reset_chat'] = True

                    # Allow the user to select a chatbot model to use
                    MODEL = st.selectbox(label='Model', options=['gpt-3.5-turbo','gpt-4'])

                # If the chat history has not yet been initialized, do so now
                if 'history' not in st.session_state:
                    st.session_state['history'] = []

                # If the chatbot is not yet ready to chat, set the "ready" flag to False
                if 'ready' not in st.session_state:
                    st.session_state['ready'] = False
                    
                # If the "reset_chat" flag has not been set, set it to False
                if 'reset_chat' not in st.session_state:
                    st.session_state['reset_chat'] = False
                
                        # If a CSV file has been uploaded
                if uploaded_file is not None:

                    # Display a spinner while processing the file
                    with st.spinner("Processing..."):

                        # Read the uploaded CSV file
                        uploaded_file.seek(0)
                        file = uploaded_file.read()
                        
                        # Generate embeddings vectors for the file
                        vectors = await getDocEmbeds(file, uploaded_file.name)

                        # Use the Langchain ConversationalRetrievalChain to set up the chatbot
                        chain = ConversationalRetrievalChain.from_llm(llm = ChatOpenAI(temperature=0.0,model_name=MODEL),
                                                                      retriever=vectors.as_retriever())

                    # Set the "ready" flag to True now that the chatbot is ready to chat
                    st.session_state['ready'] = True

                # If the chatbot is ready to chat
                if st.session_state['ready']:

                    # If the chat history has not yet been initialized, initialize it now
                    if 'generated' not in st.session_state:
                        st.session_state['generated'] = ["Hello ! Ask me anything about " + uploaded_file.name + " 🤗"]

                    if 'past' not in st.session_state:
                        st.session_state['past'] = ["Hey ! 👋"]

                    # Create a container for displaying the chat history
                    response_container = st.container()
                    
                    # Create a container for the user's text input
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

                        # If the user has submitted a query
                        if submit_button and user_input:
                            
                            # Generate a response using the Langchain ConversationalRetrievalChain
                            output = await conversational_chat(user_input)
                            
                            # Add the user's input and the chatbot's output to the chat history
                            st.session_state['past'].append(user_input)
                            st.session_state['generated'].append(output)

                    # If there are generated messages to display
                    if st.session_state['generated']:
                        
                        # Display the chat history
                        with response_container:
                            
                            for i in range(len(st.session_state['generated'])):
                                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
                #st.write(chain)

            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Create an expander for the "About" section
    about = st.sidebar.expander("About 🤖")
    
    # Write information about the chatbot in the "About" section
    about.write("#### ChatBot-CSV is an AI chatbot featuring conversational memory, designed to enable users to discuss their CSV data in a more intuitive manner. 📄")
    about.write("#### He employs large language models to provide users with seamless, context-aware natural language interactions for a better understanding of their CSV data. 🌐")
    about.write("#### Powered by [Langchain](https://github.com/hwchase17/langchain), [OpenAI](https://platform.openai.com/docs/models/gpt-3-5) and [Streamlit](https://github.com/streamlit/streamlit) ⚡")
    about.write("#### Source code : [yvann-hub/ChatBot-CSV](https://github.com/yvann-hub/ChatBot-CSV)")

#Run the main function using asyncio
if __name__ == "__main__":
    asyncio.run(main())

