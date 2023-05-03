import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
from langchain.callbacks import get_openai_callback

def count_tokens_chain(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        st.write(f'###### Tokens used in this conversation : {cb.total_tokens} tokens')

        

    return result 
class Chatbot:
    _template = """Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question.
    Chat History:
    {chat_history}
    Follow-up entry: {question}
    Standalone question:"""

    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

    qa_template = """"You are an AI conversational assistant to answer questions based on a context.
    You are given data from a csv file and a question, you must help the user find the information they need. 
    Your answers should be friendly, response to the user in his own language.
    question: {question}
    =========
    context: {context}
    =======
    """

    QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["question", "context"])

    def __init__(self, model_name, temperature, vectors):
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors



    def conversational_chat(self, query):
            """
            Starts a conversational chat with a model via Langchain
            """
            llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)
            chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                condense_question_prompt=self.CONDENSE_QUESTION_PROMPT,
                qa_prompt=self.QA_PROMPT,
                retriever=self.vectors.as_retriever(),
            )

            chain_input = {"question": query, "chat_history": st.session_state["history"]}
            result = chain(chain_input)

            st.session_state["history"].append((query, result["answer"]))
            count_tokens_chain(chain, chain_input)
            return result["answer"]


    
    
