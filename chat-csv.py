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

def qa_associations(user_secret):
    os.environ["OPENAI_API_KEY"] = user_secret
    try:
        if user_secret == "":
            st.markdown(
                "<div style='text-align: center;'><h4>Saisissez votre clé d'API OpenAI pour commencer à parler à Poto 😉</h4></div>",
                unsafe_allow_html=True
            )
        else:
            # Upload CSV file
            uploaded_file = st.sidebar.file_uploader("", type=["csv"])
            if uploaded_file is not None:
                # Show uploaded CSV file
                def show_user_file():
                    file_container = st.expander("Votre fichier CSV :")
                    shows = pd.read_csv(uploaded_file)
                    uploaded_file.seek(0)
                    file_container.write(shows)
                    
                show_user_file()
                
            else :
                st.sidebar.info(
                f"""
                    👆 Chargez un fichier .csv pour commencer, 
                    exemple : [MonAmiPoto-Associations.csv](https://drive.google.com/file/d/1l9WZo6TBleAWMdkxAAmM5fRHIU3fBpGW/view?usp=sharing)
                    """
                )
            
            if uploaded_file:
                # Save user's CSV file
                def save_user_file(uploaded_file):
                    save_folder = 'dataset'
                    save_path = Path(save_folder, uploaded_file.name)
                    with open(save_path, mode='wb') as w:
                        w.write(uploaded_file.getvalue())
                        
                    file_path_user=os.path.join('dataset/', uploaded_file.name)
                    return file_path_user
                    
                # Create retriever from user's CSV file
                def formalize_user_file_for_llm(file_path_user):
                    loader = CSVLoader(file_path=file_path_user, encoding="utf-8")
                    data = loader.load()
                    text_splitter = CharacterTextSplitter(separator="type-organisation:", chunk_size=1500, chunk_overlap=0)
                    texts = text_splitter.split_documents(data)

                    embeddings = OpenAIEmbeddings()
                    
                    db = Chroma.from_documents(texts, embeddings)
                    retriever = db.as_retriever()
                    return retriever
                
                user_file_path = save_user_file(uploaded_file)
                retriever_db = formalize_user_file_for_llm(user_file_path)
                
                # Create custom prompt for MonAmiPoto
                def adapt_llm_response_to_poto():
                    prompt_template = (
                    "You are MonAmiPoto, a friendly virtual friend assisting users with social and professional needs based on a context. "
                    "Your knowledge comes from:"

                    " {context} "

                    "provide at least one association's name and website, up to three if available. "
                    "Include a brief description and additional information (SIRET, SIREN, secteurs-interventions, email) if requested. "
                    "If no associations in your context can help the user with their specific problem or need, "
                    "empathize with their situation and clearly state that it seems MonAmiPoto doesn't have any associations to help them, "
                    "but they can look elsewhere for assistance Maintain a friendly, sympathetic tone. "
                    "If you don't know the answer to a question,"
                    "truthfully say you don't know."
                    
                    "Human: {question} "

                    "MonAmiPoto: "               
                    )

                    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context","question"])
                    chain_type_kwargs = {"prompt": PROMPT}
                    return chain_type_kwargs
                
            custom_pompt = adapt_llm_response_to_poto()

            # Initialize RetrievalQA with custom prompt and retriever
            qa = RetrievalQA.from_chain_type(llm =ChatOpenAI(temperature=0, model="gpt-3.5-turbo"), chain_type='stuff', retriever=retriever_db, chain_type_kwargs=custom_pompt)
            
            # Chatbot UI function
            def chatbot_ui(qa):
                if 'generated' not in st.session_state:
                    st.session_state['generated'] = []

                if 'past' not in st.session_state:
                    st.session_state['past'] = []

                def generate_response(query):
                    response = qa.run(query)
                    print(f"Type of response: {type(response)}, response: {response}")

                    return response

                def get_text():
                    st.write("")
                    input_text = st.text_input("##### Demandez de l'aide à Poto à partir de votre base de données 👇: ", key="input")
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
            chatbot_ui(qa)

    except Exception as e:
        st.error(f"Error: {str(e)}")

    # About section
    st.sidebar.title(" À propos...")
    st.sidebar.subheader("Mon Ami Poto est un Chat-Bot intelligent conçu pour aider l'utilisateur dans les aspects sociaux et professionnels de sa vie.") 
    st.sidebar.subheader("Pour l'aider, il s'appuie sur la base de données CSV que vous lui fournissez et sur l'API de ChatGPT.")
    st.sidebar.subheader("Développé avec Langchain et OpenAI.")

