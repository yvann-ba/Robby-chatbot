import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
from langchain.callbacks import get_openai_callback

#fix Error: module 'langchain' has no attribute 'verbose'
import langchain
langchain.verbose = False

class Chatbot:

    def __init__(self, model_name, temperature, vectors, df_dev, df_prod):
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors

    qa_template = """
        You are a helpful AI assistant named Bob. The user gives you a NSW Fairwork legislation, use them to answer the question at the end.
        If you don't know the answer, just say you don't know. Do NOT try to make up an answer.
        If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
        Use as much detail as possible when responding.

        The user also has their payroll data in a CSV, where every element is a shift penalty or annual leave. A dataset should either have shift penalties loads or 17.5% annual leave loading, whichever is higher. If a dataset has both, then it does not adhere to Clause 28.3 (a) of the legislation.

        Production Payroll Data:

        Emp Code,Payroll Code,Export Code,Export Name,Export Qty,Rate,Value,Date,Location ID,Role,Period,Event Code,Event Name,Day Start,Date Start,Time Start,Day End,Date End,Time End,Net Hours,Reversal
        73677,73677,AS15,ACA Ann L Aftn Load 15%,7.6,3.55,$26.98 ,16/5/2022,L103,Personal Care Attendant,SHIFT,,,Monday,16/5/2022,23:00,Tuesday,17/5/2022,7:06,7.6,No
        73677,73677,AS15,ACA Ann L Aftn Load 15%,7.6,3.55,$26.98 ,17/5/2022,L103,Personal Care Attendant,SHIFT,,,Tuesday,17/5/2022,23:00,Wednesday,18/5/2022,7:06,7.6,No
        73677,73677,AS15,ACA Ann L Aftn Load 15%,7.6,3.55,$26.98 ,18/5/2022,L103,Personal Care Attendant,SHIFT,,,Wednesday,18/5/2022,23:00,Thursday,19/5/2022,7:06,7.6,No
        73677,73677,AS15,ACA Ann L Aftn Load 15%,7.6,3.55,$26.98 ,23/5/2022,L103,Personal Care Attendant,SHIFT,,,Monday,23/5/2022,23:00,Tuesday,24/5/2022,7:06,7.6,No
        73677,73677,AS15,ACA Ann L Aftn Load 15%,7.6,3.55,$26.98 ,24/5/2022,L103,Personal Care Attendant,SHIFT,,,Tuesday,24/5/2022,23:00,Wednesday,25/5/2022,7:06,7.6,No
        73677,73677,AS15,ACA Ann L Aftn Load 15%,7.6,3.55,$26.98 ,25/5/2022,L103,Personal Care Attendant,SHIFT,,,Wednesday,25/5/2022,23:00,Thursday,26/5/2022,7:06,7.6,No
        73677,73677,ANSA,ACA Ann Sat Load 50%,7.6,11.84,$89.95 ,21/5/2022,L103,Personal Care Attendant,SHIFT,,,Saturday,21/5/2022,6:54,Saturday,21/5/2022,15:00,7.6,No
        73677,73677,ANSA,ACA Ann Sat Load 50%,7.6,11.84,$89.95 ,28/5/2022,L103,Personal Care Attendant,SHIFT,,,Saturday,28/5/2022,6:54,Saturday,28/5/2022,15:00,7.6,No
        73677,73677,ANSU,ACA Ann Sun Load 75%,7.6,17.75,$134.92 ,22/5/2022,L103,Personal Care Attendant,SHIFT,,,Sunday,22/5/2022,6:54,Sunday,22/5/2022,15:00,7.6,No
        73677,73677,ANSU,ACA Ann Sun Load 75%,7.6,17.75,$134.92 ,29/5/2022,L103,Personal Care Attendant,SHIFT,,,Sunday,29/5/2022,6:54,Sunday,29/5/2022,15:00,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,16/5/2022,L103,Personal Care Attendant,SHIFT,,,Monday,16/5/2022,23:00,Tuesday,17/5/2022,7:06,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,17/5/2022,L103,Personal Care Attendant,SHIFT,,,Tuesday,17/5/2022,23:00,Wednesday,18/5/2022,7:06,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,18/5/2022,L103,Personal Care Attendant,SHIFT,,,Wednesday,18/5/2022,23:00,Thursday,19/5/2022,7:06,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,21/5/2022,L103,Personal Care Attendant,SHIFT,,,Saturday,21/5/2022,6:54,Saturday,21/5/2022,15:00,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,22/5/2022,L103,Personal Care Attendant,SHIFT,,,Sunday,22/5/2022,6:54,Sunday,22/5/2022,15:00,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,23/5/2022,L103,Personal Care Attendant,SHIFT,,,Monday,23/5/2022,23:00,Tuesday,24/5/2022,7:06,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,24/5/2022,L103,Personal Care Attendant,SHIFT,,,Tuesday,24/5/2022,23:00,Wednesday,25/5/2022,7:06,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,25/5/2022,L103,Personal Care Attendant,SHIFT,,,Wednesday,25/5/2022,23:00,Thursday,26/5/2022,7:06,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,28/5/2022,L103,Personal Care Attendant,SHIFT,,,Saturday,28/5/2022,6:54,Saturday,28/5/2022,15:00,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,29/5/2022,L103,Personal Care Attendant,SHIFT,,,Sunday,29/5/2022,6:54,Sunday,29/5/2022,15:00,7.6,No

        Total weekend and shift penalties (Production): 611.62
        Total annual leave (Production): 1799.10
        Total annual leave loading (Production): 0

        Development Payroll Data:

        Emp Code,Payroll Code,Export Code,Export Name,Export Qty,Rate,Value,Date,Location ID,Role,Period,Event Code,Event Name,Day Start,Date Start,Time Start,Day End,Date End,Time End,Net Hours,Reversal
        73677,73677,AS15,ACA Ann L Aftn Load 15%,7.6,3.55,$26.98 ,16/5/2022,L103,Personal Care Attendant,SHIFT,,,Monday,16/5/2022,23:00,Tuesday,17/5/2022,7:06,7.6,No
        73677,73677,AS15,ACA Ann L Aftn Load 15%,7.6,3.55,$26.98 ,17/5/2022,L103,Personal Care Attendant,SHIFT,,,Tuesday,17/5/2022,23:00,Wednesday,18/5/2022,7:06,7.6,No
        73677,73677,AS15,ACA Ann L Aftn Load 15%,7.6,3.55,$26.98 ,18/5/2022,L103,Personal Care Attendant,SHIFT,,,Wednesday,18/5/2022,23:00,Thursday,19/5/2022,7:06,7.6,No
        73677,73677,AS15,ACA Ann L Aftn Load 15%,7.6,3.55,$26.98 ,23/5/2022,L103,Personal Care Attendant,SHIFT,,,Monday,23/5/2022,23:00,Tuesday,24/5/2022,7:06,7.6,No
        73677,73677,AS15,ACA Ann L Aftn Load 15%,7.6,3.55,$26.98 ,24/5/2022,L103,Personal Care Attendant,SHIFT,,,Tuesday,24/5/2022,23:00,Wednesday,25/5/2022,7:06,7.6,No
        73677,73677,AS15,ACA Ann L Aftn Load 15%,7.6,3.55,$26.98 ,25/5/2022,L103,Personal Care Attendant,SHIFT,,,Wednesday,25/5/2022,23:00,Thursday,26/5/2022,7:06,7.6,No
        73677,73677,ANSA,ACA Ann Sat Load 50%,7.6,11.84,$89.95 ,21/5/2022,L103,Personal Care Attendant,SHIFT,,,Saturday,21/5/2022,6:54,Saturday,21/5/2022,15:00,7.6,No
        73677,73677,ANSA,ACA Ann Sat Load 50%,7.6,11.84,$89.95 ,28/5/2022,L103,Personal Care Attendant,SHIFT,,,Saturday,28/5/2022,6:54,Saturday,28/5/2022,15:00,7.6,No
        73677,73677,ANSU,ACA Ann Sun Load 75%,7.6,17.75,$134.92 ,22/5/2022,L103,Personal Care Attendant,SHIFT,,,Sunday,22/5/2022,6:54,Sunday,22/5/2022,15:00,7.6,No
        73677,73677,ANSU,ACA Ann Sun Load 75%,7.6,17.75,$134.92 ,29/5/2022,L103,Personal Care Attendant,SHIFT,,,Sunday,29/5/2022,6:54,Sunday,29/5/2022,15:00,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,16/5/2022,L103,Personal Care Attendant,SHIFT,,,Monday,16/5/2022,23:00,Tuesday,17/5/2022,7:06,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,17/5/2022,L103,Personal Care Attendant,SHIFT,,,Tuesday,17/5/2022,23:00,Wednesday,18/5/2022,7:06,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,18/5/2022,L103,Personal Care Attendant,SHIFT,,,Wednesday,18/5/2022,23:00,Thursday,19/5/2022,7:06,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,21/5/2022,L103,Personal Care Attendant,SHIFT,,,Saturday,21/5/2022,6:54,Saturday,21/5/2022,15:00,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,22/5/2022,L103,Personal Care Attendant,SHIFT,,,Sunday,22/5/2022,6:54,Sunday,22/5/2022,15:00,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,23/5/2022,L103,Personal Care Attendant,SHIFT,,,Monday,23/5/2022,23:00,Tuesday,24/5/2022,7:06,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,24/5/2022,L103,Personal Care Attendant,SHIFT,,,Tuesday,24/5/2022,23:00,Wednesday,25/5/2022,7:06,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,25/5/2022,L103,Personal Care Attendant,SHIFT,,,Wednesday,25/5/2022,23:00,Thursday,26/5/2022,7:06,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,28/5/2022,L103,Personal Care Attendant,SHIFT,,,Saturday,28/5/2022,6:54,Saturday,28/5/2022,15:00,7.6,No
        73677,73677,ANN,ACA Annual Leave,7.6,23.67,$179.91 ,29/5/2022,L103,Personal Care Attendant,SHIFT,,,Sunday,29/5/2022,6:54,Sunday,29/5/2022,15:00,7.6,No
        73677,73677,ALVD,ACA Leave Load 17.5%,7.6,3.66,$27.80 ,16/5/2022,L094,Personal Care Attendant,SHIFT,,,Monday,16/5/2022,23:00,Tuesday,17/5/2022,7:06,7.6,No
        73677,73677,ALVD,ACA Leave Load 17.5%,7.6,3.66,$27.80 ,17/5/2022,L094,Personal Care Attendant,SHIFT,,,Tuesday,17/5/2022,23:00,Wednesday,18/5/2022,7:06,7.6,No
        73677,73677,ALVD,ACA Leave Load 17.5%,7.6,3.66,$27.80 ,18/5/2022,L094,Personal Care Attendant,SHIFT,,,Wednesday,18/5/2022,23:00,Thursday,19/5/2022,7:06,7.6,No
        73677,73677,ALVD,ACA Leave Load 17.5%,7.6,3.66,$27.80 ,21/5/2022,L103,Personal Care Attendant,SHIFT,,,Saturday,21/5/2022,6:54,Saturday,21/5/2022,15:00,7.6,No
        73677,73677,ALVD,ACA Leave Load 17.5%,7.6,3.66,$27.80 ,22/5/2022,L103,Personal Care Attendant,SHIFT,,,Sunday,22/5/2022,6:54,Sunday,22/5/2022,15:00,7.6,No
        73677,73677,ALVD,ACA Leave Load 17.5%,7.6,3.66,$27.80 ,23/5/2022,L094,Personal Care Attendant,SHIFT,,,Monday,23/5/2022,23:00,Tuesday,24/5/2022,7:06,7.6,No
        73677,73677,ALVD,ACA Leave Load 17.5%,7.6,3.66,$27.80 ,24/5/2022,L094,Personal Care Attendant,SHIFT,,,Tuesday,24/5/2022,23:00,Wednesday,25/5/2022,7:06,7.6,No
        73677,73677,ALVD,ACA Leave Load 17.5%,7.6,3.66,$27.80 ,25/5/2022,L094,Personal Care Attendant,SHIFT,,,Wednesday,25/5/2022,23:00,Thursday,26/5/2022,7:06,7.6,No
        73677,73677,ALVD,ACA Leave Load 17.5%,7.6,3.66,$27.80 ,28/5/2022,L103,Personal Care Attendant,SHIFT,,,Saturday,28/5/2022,6:54,Saturday,28/5/2022,15:00,7.6,No
        73677,73677,ALVD,ACA Leave Load 17.5%,7.6,3.66,$27.80 ,29/5/2022,L103,Personal Care Attendant,SHIFT,,,Sunday,29/5/2022,6:54,Sunday,29/5/2022,15:00,7.6,No

        Total weekend and shift penalties (dev): 611.62
        Total annual leave (dev): 1799.10
        Total annual leave loading (dev): 278

        For context, the shift penalties are represented by the following Export Name:
        1. ACA Ann Morn Load 10%
        2. ACA Ann Aftn Load 12.5%
        3. ACA Ann L Aftn Load 15%
        4. ACA Ann E Morn Load 10%

        ACA Leave Load 17.5% is the special annual leave loading of 17.5%. 

        context: {context}
        =========
        question: {question}
        ======
        """

    QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["context","question", "df_prod", "df_dev"])

    def conversational_chat(self, query, df_dev, df_prod):
        """
        Start a conversational chat with a model via Langchain
        """
        llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)

        retriever = self.vectors.as_retriever()


        chain = ConversationalRetrievalChain.from_llm(llm=llm,
            retriever=retriever, 
            verbose=True, 
            return_source_documents=True, 
            max_tokens_limit=16384, 
            combine_docs_chain_kwargs={'prompt': self.QA_PROMPT})

        chain_input = {"question": query, 
                       "chat_history": st.session_state["history"],
                       "df_prod": df_prod,
                       "df_dev": df_dev,
                       }
        result = chain(chain_input)

        st.session_state["history"].append((query, result["answer"]))
        #count_tokens_chain(chain, chain_input)
        return result["answer"]


def count_tokens_chain(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        st.write(f'###### Tokens used in this conversation : {cb.total_tokens} tokens')
    return result 

    
    
