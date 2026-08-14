import streamlit as st

from rag import generate_answer
from updater import update_knowledge_base


# Page configuration
st.set_page_config(
    page_title="Dynamic Knowledge Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 Dynamic Knowledge Base Chatbot")

st.write(
    "Ask questions about the information stored "
    "in the chatbot's knowledge base."
)

st.info(
    "The knowledge base can be updated with new "
    "information without retraining the chatbot."
)


# Update Knowledge Base button
if st.button("🔄 Update Knowledge Base"):

    with st.spinner("Checking for new information..."):

        try:
            update_knowledge_base()

            st.success(
                "Knowledge base updated successfully!"
            )

        except Exception as e:

            st.error(
                f"Error while updating knowledge base: {e}"
            )


# User question
question = st.text_input(
    "Enter your question:"
)


# Generate answer
if question:

    with st.spinner("Searching knowledge base..."):

        try:

            answer = generate_answer(question)

            st.subheader("Answer")

            st.write(answer)

        except Exception as e:

            st.error(
                f"Error while generating answer: {e}"
            )