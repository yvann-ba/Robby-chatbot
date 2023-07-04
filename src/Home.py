import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Config
st.set_page_config(layout="wide", page_icon="💬", page_title="Isabella | Chat-Bot 🤖")

# Contact
with st.sidebar.expander("📬 Contact"):
    st.markdown("**GitHub:** [yvann-hub/Robby-chatbot](https://github.com/yvann-hub/Robby-chatbot)")
    st.markdown("**Medium:** [@yvann-hub](https://medium.com/@yvann-hub)")
    st.markdown("**Twitter:** [@yvann_hub](https://twitter.com/yvann_hub)")
    st.markdown("**Mail** : barbot.yvann@gmail.com")
    st.markdown("**Created by Yvann**")

# Title
st.markdown("<h2 style='text-align: center;'>Isabella, your data-aware assistant 🤖</h1>", unsafe_allow_html=True)
st.markdown("---")

# Description
st.markdown(
    """ 
    <h5 style='text-align:center;'>I'm Isabella, an intelligent chatbot created by combining 
    the strengths of Langchain and Streamlit. I use large language models to provide
    context-sensitive interactions. My goal is to help you better understand your data.
    I support PDF, TXT, CSV, Youtube transcript 🧠</h5>
    """,
    unsafe_allow_html=True)
st.markdown("---")

# Isabella's Pages
st.subheader("🚀 Isabella's Pages")
st.markdown("""
- **Isabella-Chat**: General Chat on data (PDF, TXT,CSV) with a [vectorstore](https://github.com/facebookresearch/faiss) (index useful parts(max 4) for respond to the user) | works with [ConversationalRetrievalChain](https://python.langchain.com/en/latest/modules/chains/index_examples/chat_vector_db.html)
- **Isabella-Sheet** (beta): Chat on tabular data (CSV) | for precise information | process the whole file | works with [CSV_Agent](https://python.langchain.com/en/latest/modules/agents/toolkits/examples/csv.html) + [PandasAI](https://github.com/gventuri/pandas-ai) for data manipulation and graph creation
- **Isabella-Youtube**: Summarize YouTube videos with [summarize-chain](https://python.langchain.com/en/latest/modules/chains/index_examples/summarize.html)
""")
st.markdown("---")

# Contributing
st.markdown("### 🎯 Contributing")
st.markdown("Isabella is under regular development. Feel free to contribute and help me make it even more data-aware!", unsafe_allow_html=True)
