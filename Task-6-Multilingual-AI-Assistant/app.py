import streamlit as st
import ollama
from reasoning_engine import validate_response
from PIL import Image
import io
from langdetect import detect


# --------------------------------------------------
# LANGUAGE DETECTION
# --------------------------------------------------

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi",
    "es": "Spanish"
}


def detect_language(text):

    text_lower = text.lower().strip()

    # Spanish keyword detection
    spanish_words = [
        "qué", "cómo", "dónde", "cuándo", "por qué",
        "esta", "este", "imagen", "puede", "pueden",
        "ver", "gráfico", "pregunta", "respuesta",
        "hola", "gracias", "segmento", "más pequeño"
    ]

    spanish_score = sum(
        1 for word in spanish_words
        if word in text_lower
    )

    if spanish_score >= 2:
        return "Spanish"

    # Hindi / Marathi detection
    if any("\u0900" <= char <= "\u097F" for char in text):

        try:
            code = detect(text)

            if code == "mr":
                return "Marathi"

            if code == "hi":
                return "Hindi"

        except Exception:
            pass

    # General detection
    try:
        code = detect(text)
        return LANGUAGE_NAMES.get(code, "English")

    except Exception:
        return "English"


# --------------------------------------------------
# IMAGE CONVERSION
# --------------------------------------------------

def image_to_bytes(image):

    buffer = io.BytesIO()

    if image.mode != "RGB":
        image = image.convert("RGB")

    image.save(buffer, format="JPEG")

    return buffer.getvalue()


# --------------------------------------------------
# IMAGE ANALYSIS
# --------------------------------------------------

def analyze_image(image, question, history, detected_language):

    image_bytes = image_to_bytes(image)

    prompt = f"""
You are a multilingual multimodal AI assistant.

IMPORTANT:
The uploaded image is the SAME image being discussed throughout
this conversation.

You MUST look at the uploaded image before answering.

The user may ask follow-up questions about the same image.
Even if the current question is short, ambiguous, or mixed-language,
use BOTH:
1. The uploaded image
2. The previous conversation

to understand the user's intended question.

USER QUESTION:
{question}

DETECTED LANGUAGE:
{detected_language}

PREVIOUS CONVERSATION:
{history}

TASK:

1. Carefully analyze the uploaded image.
2. Understand the user's current question.
3. Use previous conversation to maintain context.
4. If the user refers to "it", "that", "the smallest one",
   "the largest one", "उसका", "त्याचा", "ese", "ese segmento",
   or similar words, identify the correct object from the
   previous conversation and the image.
5. Understand mixed-language questions such as:
   "इस image में सबसे छोटा segment कौन सा है?"
6. Preserve the user's intent when switching between languages.
7. Resolve ambiguity using the image and conversation context.
8. Do not invent visual information.
9. Give an evidence-based answer.
10. Answer completely in the detected language.

The image is available to you.
Do NOT say that you cannot see the image.
Do NOT ask the user to describe the image if the answer
can be obtained from the uploaded image.

Return only the answer to the user's question.
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


# --------------------------------------------------
# STREAMLIT PAGE
# --------------------------------------------------

st.set_page_config(
    page_title="Multilingual AI Assistant",
    page_icon="🌍",
    layout="wide"
)


st.title("🌍 Multilingual Multimodal AI Assistant")

st.write(
    "An AI assistant that understands images, multiple languages, "
    "mixed-language questions, and conversation context."
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "image" not in st.session_state:
    st.session_state.image = None


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    st.write("Supported languages:")

    st.write("🇬🇧 English")
    st.write("🇮🇳 Hindi")
    st.write("🇮🇳 Marathi")
    st.write("🇪🇸 Spanish")

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file is not None:

        st.session_state.image = Image.open(uploaded_file)

        st.image(
            st.session_state.image,
            caption="Uploaded Image",
            use_container_width=True
        )

    st.divider()

    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = []
        st.session_state.image = None

        st.rerun()


# --------------------------------------------------
# DISPLAY PREVIOUS CONVERSATION
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "user" and "language" in message:

            st.caption(
                f"🌐 Detected language: {message['language']}"
            )


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

question = st.chat_input(
    "Ask in English, Hindi, Marathi, Spanish, or mixed language..."
)


if question:

    # ----------------------------------------------
    # LANGUAGE DETECTION
    # ----------------------------------------------

    detected_language = detect_language(question)


    # ----------------------------------------------
    # SAVE USER MESSAGE
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
            "language": detected_language
        }
    )


    # ----------------------------------------------
    # DISPLAY USER MESSAGE
    # ----------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)

        st.caption(
            f"🌐 Detected language: {detected_language}"
        )


    # ----------------------------------------------
    # PREPARE CONVERSATION HISTORY
    # ----------------------------------------------

    history = []

    for message in st.session_state.messages[:-1]:

        history.append(
            f"{message['role']}: {message['content']}"
        )

    history_text = "\n".join(history)


    # ----------------------------------------------
    # IMAGE AVAILABLE
    # ----------------------------------------------

    if st.session_state.image is not None:

        with st.chat_message("assistant"):

            with st.spinner(
                "Analyzing image and reasoning..."
            ):

                try:

                    draft_answer = analyze_image(
                        st.session_state.image,
                        question,
                        history_text,
                        detected_language
                    )


                    # ----------------------------------
                    # RESPONSE VALIDATION
                    # ----------------------------------

                    final_answer = validate_response(
                        question,
                        draft_answer,
                        history_text,
                        detected_language
                    )


                    st.markdown(final_answer)


                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": final_answer
                        }
                    )


                except Exception as e:

                    st.error(
                        f"Error while processing the request: {e}"
                    )


    # ----------------------------------------------
    # TEXT-ONLY CHAT
    # ----------------------------------------------

    else:

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    prompt = f"""
You are a multilingual AI assistant.

USER QUESTION:
{question}

DETECTED LANGUAGE:
{detected_language}

PREVIOUS CONVERSATION:
{history_text}

Instructions:

1. Understand the user's intent.
2. Maintain conversation context.
3. Support English, Hindi, Marathi, and Spanish.
4. Understand mixed-language questions.
5. Resolve ambiguous questions using previous context.
6. Preserve meaning when the user switches languages.
7. Give an evidence-based answer.
8. Answer completely in the detected language.
"""

                    response = ollama.chat(
                        model="llama3:latest",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                    draft_answer = response["message"]["content"]


                    # ----------------------------------
                    # RESPONSE VALIDATION
                    # ----------------------------------

                    final_answer = validate_response(
                        question,
                        draft_answer,
                        history_text,
                        detected_language
                    )


                    st.markdown(final_answer)


                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": final_answer
                        }
                    )


                except Exception as e:

                    st.error(
                        f"Error while processing the request: {e}"
                    )