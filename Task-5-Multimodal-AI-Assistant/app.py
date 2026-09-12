import streamlit as st
import ollama
from reasoning_engine import validate_response
from PIL import Image
import io


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Multimodal AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multimodal AI Assistant")
st.caption("Text + Image Understanding with Contextual Reasoning")


# -----------------------------
# Session State
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "image_context" not in st.session_state:
    st.session_state.image_context = None


# -----------------------------
# Convert Image to Bytes
# -----------------------------

def image_to_bytes(image):
    buffer = io.BytesIO()

    if image.mode != "RGB":
        image = image.convert("RGB")

    image.save(buffer, format="JPEG")

    return buffer.getvalue()


# -----------------------------
# Analyze Image using Qwen3-VL
# -----------------------------

def analyze_image(image, question, history):

    image_bytes = image_to_bytes(image)

    history_text = ""

    for message in history[-6:]:
        history_text += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    prompt = f"""
You are a multimodal AI assistant.

You can understand both images and text.

Your task is to carefully analyze the uploaded image and answer
the user's question using visual evidence.

Important rules:

1. First identify what can actually be observed in the image.
2. Do not invent objects, text, people, numbers, or events.
3. Separate direct observations from assumptions.
4. If something is unclear, say that it is unclear.
5. Use previous conversation context when relevant.
6. If the user's question is ambiguous, explain the ambiguity
   and make the most reasonable interpretation.
7. Give an evidence-based answer.
8. Explain your reasoning when it helps the user understand
   the decision.
9. Do not claim information that cannot be supported by the image
   or conversation.

Previous Conversation:

{history_text}

Current User Question:

{question}

Analyze the image carefully and provide a useful answer.
"""

    response = ollama.chat(
        model="qwen3-vl:4b",
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [image_bytes]
            }
        ]
    )

    return response["message"]["content"]


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("⚙️ Controls")

    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = []
        st.session_state.image_context = None

        st.rerun()

    st.divider()

    st.subheader("AI Models")

    st.write("👁️ Vision Model")
    st.code("Qwen3-VL 4B")

    st.write("🔍 Validation Model")
    st.code("Llama 3")

    st.divider()

    st.info(
        "Upload an image and ask questions about it. "
        "The assistant analyzes the image first and then "
        "validates the generated response."
    )


# -----------------------------
# Image Upload
# -----------------------------

st.subheader("📷 Upload Image")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file is not None:

    current_uploaded_image = Image.open(uploaded_file)

    st.session_state.image_context = current_uploaded_image

    st.image(
        current_uploaded_image,
        caption="Uploaded Image",
        use_container_width=True
    )

    st.success("Image uploaded successfully.")


# -----------------------------
# Conversation History
# -----------------------------

if st.session_state.messages:

    st.subheader("💬 Conversation")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])


# -----------------------------
# Chat Input
# -----------------------------

question = st.chat_input(
    "Ask a question about the image..."
)


# -----------------------------
# Process User Question
# -----------------------------

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)

    # -------------------------
    # Check Image
    # -------------------------

    if st.session_state.image_context is None:

        answer = (
            "⚠️ I don't currently have an image to analyze. "
            "Please upload an image first."
        )

        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    else:

        try:

            current_image = st.session_state.image_context

            # -------------------------
            # Stage 1: Vision Analysis
            # -------------------------

            with st.chat_message("assistant"):

                with st.spinner(
                    "🧠 Analyzing image and reasoning..."
                ):

                    draft_answer = analyze_image(
                        current_image,
                        question,
                        st.session_state.messages[:-1]
                    )

                # -------------------------
                # Stage 2: Response Validation
                # -------------------------

                with st.spinner(
                    "🔍 Validating response..."
                ):

                    answer = validate_response(
                        question,
                        draft_answer,
                        st.session_state.messages[:-1]
                    )

                st.write(answer)

            # -------------------------
            # Save Final Answer
            # -------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:

            error_message = (
                f"❌ An error occurred:\n\n{str(e)}"
            )

            with st.chat_message("assistant"):
                st.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message
                }
            )


# -----------------------------
# How It Works
# -----------------------------

st.divider()

st.subheader("🧠 How It Works")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        """
        ### 1️⃣ Image Input

        The user uploads an image
        and asks a question.
        """
    )


with col2:

    st.markdown(
        """
        ### 2️⃣ Vision Analysis

        **Qwen3-VL 4B** analyzes
        the image and creates
        a draft answer.
        """
    )


with col3:

    st.markdown(
        """
        ### 3️⃣ Response Validation

        **Llama 3** checks the
        response for unsupported
        assumptions and errors.
        """
    )


with col4:

    st.markdown(
        """
        ### 4️⃣ Final Answer

        The validated response
        is shown to the user.
        """
    )