import streamlit as st
from langchain_helper import get_qa_chain, create_vector_db

st.title("CUSTOMER SERVICE CHATBOT 🤖")

question = st.text_input("Question:")

if question:
    try:
        chain = get_qa_chain()

        with st.spinner("Generating answer..."):
            response = chain(question)

        st.subheader("Answer")
        st.write(response)

    except Exception as e:
        st.error("Something went wrong:")
        st.exception(e)