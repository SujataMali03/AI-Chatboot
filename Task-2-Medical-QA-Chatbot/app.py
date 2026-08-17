import streamlit as st

from src.qa_engine import ask_question
from src.entity_recognition import find_entities, detect_question_type


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Medical Q&A Chatbot",
    page_icon="🩺",
    layout="centered"
)


# --------------------------------------------------
# Session State - Chat History
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🩺 Medical Q&A Chatbot")

st.write(
    "Ask medical questions and retrieve relevant "
    "answers from the MedQuAD knowledge base."
)

st.warning(
    "⚠️ Educational information only. This chatbot is "
    "not a substitute for professional medical advice, "
    "diagnosis, or treatment."
)


# --------------------------------------------------
# Display Previous Chat
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["role"] == "user":

            st.write(message["content"])

        else:

            result = message["result"]

            if result["found"]:

                st.write("### 💬 Answer")

                st.write(result["answer"])

                st.write(
                    f"**Similarity:** "
                    f"{result['score']:.2%}"
                )

                st.write(
                    f"**Medical Focus:** "
                    f"{result['focus']}"
                )

            else:

                st.error(result["answer"])


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

question = st.chat_input(
    "Ask a medical question..."
)


# --------------------------------------------------
# Process Question
# --------------------------------------------------

if question:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Entity Recognition
    entities = find_entities(question)

    # Question Classification
    question_type = detect_question_type(question)

    # Retrieval
    result = ask_question(question)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "result": result,
        "entities": entities,
        "question_type": question_type
    })

    # Refresh page
    st.rerun()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("🧬 About")

    st.write(
        "This Medical Q&A Chatbot uses the "
        "MedQuAD dataset to retrieve relevant "
        "medical answers."
    )

    st.subheader("Technology")

    st.write("• Python")
    st.write("• MedQuAD Dataset")
    st.write("• TF-IDF")
    st.write("• Cosine Similarity")
    st.write("• Basic Medical NER")
    st.write("• Streamlit")

    st.divider()

    st.subheader("⚠️ Disclaimer")

    st.write(
        "The chatbot is intended for educational "
        "purposes only. Always consult a qualified "
        "healthcare professional for medical advice."
    )

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()