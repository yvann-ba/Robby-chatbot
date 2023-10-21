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

        The user also has their payroll data in a CSV, where every element is a shift penalty or annual leave. A dataset must either have shift penalties loads or 17.5% annual leave loading, whichever is higher. If a dataset has both, then it does not adhere to Clause 28.3 (a) of the legislation.

        Production Payroll Data:

        {df_prod}

        Total weekend and shift penalties (prod]): 611.62
        Total annual leave (prod): 1799.10
        Total annual leave loading (prod): 0

        Development Payroll Data:

        {df_dev}

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

        prod_string = df_prod
        dev_string = df_dev
        print(dev_string)
        chain_input = {"question": query, 
                       "chat_history": st.session_state["history"],
                       "df_prod": prod_string,
                       "df_dev": dev_string,
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

    
    
