import streamlit as st


#Config
st.set_page_config(layout="wide", page_icon="💬", page_title="Bob | Compliance-Bot 🤑")


#Contact
with st.sidebar.expander("📬 Contact"):

    st.write("**GitHub:**","[ivan-pua/sxsw-hackathon](https://github.com/ivan-pua/sxsw-hackathon)")

    st.write("**Blog:** ""[ivanpua.com](https://ivanpua.com/)")

    st.write("**Mail** : qieshang@gmail.com")
    st.write("**Created by Ivan, credits to [Yvann](https://twitter.com/yvann_hub)**")


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
    Bob's mission is to ensure payroll compliance by comparing actual employee salary against 
    expected salary. Any discrepancies are cross-checked with the NSW Fairwork legislation. 🧠</h5>
    """,
    unsafe_allow_html=True)
st.markdown("---")


#Robby's Pages
st.subheader("🚀 What Are We Solving?")
st.write("""
- **Problem**: Large enterprises like 7-Eleven have been fined millions of dollars for underpaying their employees. Whether intentional or not, this has not only lead to massive fines, significant financial losses as a result of poor reputation, and low morale among employees.
- **How it works**: Bob, powered by Langchain, uses OpenAI's GPT-3 model to chat on tabular data (CSV). It extracts the most up-to-date legislation from NSW Fairwork website to check for compliance. The entire application is built using Streamlit.
- **Features**: Bob supports CSV format as employee payroll dataset.
""")
st.markdown("---")


#Contributing
st.markdown("### 🎯 Contributing")
st.markdown("""
**Bob is under regular development. Feel free to contribute and help me make it even more data-aware!**
""", unsafe_allow_html=True)





