import streamlit as st


#Config
st.set_page_config(layout="wide", page_icon="💬", page_title="Bob | Compliance-Bot 🤖")


#Contact
with st.sidebar.expander("📬 Contact"):

    st.write("**GitHub:**",
"[yvann-hub/Robby-chatbot](https://github.com/yvann-hub/Robby-chatbot)")

    st.write("**Medium:** "
"[@yvann-hub](https://medium.com/@yvann-hub)")

    st.write("**Twitter:** [@yvann_hub](https://twitter.com/yvann_hub)")
    st.write("**Mail** : barbot.yvann@gmail.com")
    st.write("**Created by Yvann**")


#Title
st.markdown(
    """
    <h2 style='text-align: center;'>Bob, Your Payroll Compliance Buddy 🤑</h1>
    """,
    unsafe_allow_html=True,)

st.markdown("---")


#Description
st.markdown(
    """ 
    <h5 style='text-align:center;'>Meet Bob, your intelligent payroll compliance assistant. 
    Bob's mission is to ensure payroll compliance by comparing actual employee pay against 
    predicted pay. Any discrepancies are cross-checked with the NSW Fairwork legislation. 🧠</h5>
    """,
    unsafe_allow_html=True)
st.markdown("---")


#Robby's Pages
st.subheader("🚀 What are solving?")
st.write("""
- **Problem**: Large enterprises like 7-Eleven have been fined millions of dollars for underpaying their employees, a practice also known as wage theft. This not only leads to significant financial losses but also stains their reputation.
- **How it works**: Bob, powered by Langchain, uses OpenAI's GPT-3 model to chat on tabular data (CSV). It processes the entire file for precise information retrieval. The entire application is built using Streamlit.
- **Features**: Bob supports employee payroll data in CSV.
""")
st.markdown("---")


#Contributing
st.markdown("### 🎯 Contributing")
st.markdown("""
**Bob is under regular development. Feel free to contribute and help me make it even more data-aware!**
""", unsafe_allow_html=True)





