from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from textblob import TextBlob

# Load environment variables
load_dotenv()

# Get API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini model
model = genai.GenerativeModel("gemini-3.1-flash-lite")

# Start chat
chat = model.start_chat(history=[])


# -------------------------------
# SENTIMENT ANALYSIS
# -------------------------------

def analyze_sentiment(text):

    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.1:
        return "Positive"

    elif polarity < -0.1:
        return "Negative"

    else:
        return "Neutral"


# -------------------------------
# CHATBOT RESPONSE
# -------------------------------

def get_response(user_message, sentiment):

    prompt = f"""
You are a professional customer service chatbot.

Customer message:
{user_message}

Customer sentiment:
{sentiment}

Respond according to the customer's sentiment.

If the sentiment is Positive:
- Be friendly and appreciative.
- Thank the customer.

If the sentiment is Negative:
- Be empathetic.
- Apologize when appropriate.
- Acknowledge the customer's problem.
- Offer helpful assistance.

If the sentiment is Neutral:
- Give a clear and professional answer.

Keep the response short and helpful.
"""

    response = chat.send_message(prompt)

    return response.text


# -------------------------------
# STREAMLIT UI
# -------------------------------

st.set_page_config(
    page_title="Customer Service Chatbot",
    page_icon="🤖"
)

st.title("🤖 Customer Service Chatbot")
st.write("Customer service chatbot with sentiment analysis")


user_message = st.text_input(
    "Enter your message:"
)

if st.button("Send"):

    if user_message.strip() == "":
        st.warning("Please enter a message.")

    else:

        # Detect sentiment
        sentiment = analyze_sentiment(user_message)

        st.subheader("Detected Sentiment")

        if sentiment == "Positive":
            st.success("😊 Positive")

        elif sentiment == "Negative":
            st.error("😞 Negative")

        else:
            st.info("😐 Neutral")

        # Generate response
        response = get_response(
            user_message,
            sentiment
        )

        st.subheader("🤖 Chatbot Response")

        st.write(response)