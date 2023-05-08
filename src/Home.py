import streamlit as st


st.set_page_config(layout="wide", page_icon="💬", page_title="Robby | Chat-Bot 🤖")

with st.sidebar.expander("📬 Contact"):

    st.write("**GitHub:**",
"[yvann-hub/Robby-chatbot](https://github.com/yvann-hub/Robby-chatbot)")

    st.write("**Medium:** "
"[@yvann-hub](https://medium.com/@yvann-hub)")

    st.write("**Twitter:** [@yvann_hub](https://twitter.com/yvann_hub)")
    st.write("**Mail** : barbot.yvann@gmail.com")
    st.write("**Created by Yvann**")

st.markdown(
    """
    <h2 style='text-align: center;'>Robby, your data-aware assistant 🤖</h1>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown(
    """ 
    <h5 style='text-align:center;'>I'm Robby, an intelligent chatbot created by combining 
    the strengths of Langchain and Streamlit. I use large language models to provide
    context-sensitive natural language interactions. My goal is to help you better understand your data.
    I support PDF, TXT, and CSV data, with more coming soon! 🧠</h5>
    """,
    unsafe_allow_html=True)
st.markdown("---")

st.subheader("🚀 Robby's Pages")
st.write("""
- **Robby-Chat**: General Chat on data (PDF, TXT,CSV) with a [vectorstore](https://github.com/facebookresearch/faiss) (can't process the whole file just index useful parts(max 4) for respond to the user ) | works with [ConversationalRetrievalChain](https://python.langchain.com/en/latest/modules/chains/index_examples/chat_vector_db.html) + (soon) Summarize data
- **Robby-Sheet**: Chat on tabular data (CSV) | for precise information | can process the whole file (with python code) | works with [CSV_Agent](https://python.langchain.com/en/latest/modules/agents/toolkits/examples/csv.html) + [PandasAI](https://github.com/gventuri/pandas-ai) for data manipulation and graph creation (experimental)
- (soon) **Robby-Youtube**: Chat on YouTube videos
- (soon) **Robby-Lyrics**: Chat and analyze music lyrics | works by scraping lyrics from Genius
- (soon) **Robby-Github**: Chat over GitHub repositories for understanding the code
- (soon) **Robby-Website**: Chat with any website you provide
""")
st.markdown("---")

st.markdown("### 🎯 Contributing")
st.markdown("""
**Robby is under regular development. Feel free to contribute and help me make it even more data-aware!**
""", unsafe_allow_html=True)





