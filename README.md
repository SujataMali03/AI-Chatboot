# 🤖 Customer Service Chatbot with Sentiment Analysis

## Project Overview

This project is an enhancement of the Customer Service Chatbot developed
during the training program.

As part of the internship task, sentiment analysis was integrated into the
existing chatbot to detect customer emotions and generate appropriate
responses.

The chatbot classifies customer messages into:

- 😊 Positive
- 😞 Negative
- 😐 Neutral

The detected sentiment is then provided to the Gemini-powered chatbot so that
the response can be adapted to the customer's emotional state.

---

## 🎯 Internship Task

### Task 1: Sentiment Analysis Integration

Integrate sentiment analysis into the chatbot to detect and respond
appropriately to customer emotions during interactions.

### Expected Outcome

A chatbot that can recognize and address:

- Positive sentiment
- Negative sentiment
- Neutral sentiment

---

## 🔨 Implementation

The internship feature was implemented as an additional feature on the
existing training project.

### Workflow

Customer Message
↓
Sentiment Analysis
↓
Positive / Negative / Neutral
↓
Gemini AI
↓
Sentiment-aware Response

---

## ✨ Features

### Existing Training Project

- Customer service chatbot
- AI-generated responses
- Streamlit interface
- Google Gemini integration

### Internship Enhancement

- Sentiment detection using TextBlob
- Positive sentiment detection
- Negative sentiment detection
- Neutral sentiment detection
- Sentiment-aware responses
- Customer-friendly responses for negative emotions

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- TextBlob
- python-dotenv

---

## 🧪 Testing

### Test 1 — Positive

**Input:**

I am very happy with your service. Thank you for helping me!

**Detected Sentiment:**

😊 Positive

**Expected Behaviour:**

The chatbot responds in a friendly and appreciative manner.

---

### Test 2 — Negative

**Input:**

I am very disappointed with your service. My problem is still not solved.

**Detected Sentiment:**

😞 Negative

**Expected Behaviour:**

The chatbot acknowledges the customer's frustration, apologizes when
appropriate, and offers assistance.

---

### Test 3 — Neutral

**Input:**

What are your customer service working hours?

**Detected Sentiment:**

😐 Neutral

**Expected Behaviour:**

The chatbot provides a clear and professional answer.

---

## 📂 Project Structure

customer_service_chatbot/
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md

---

## ▶️ How to Run

### 1. Install dependencies

pip install -r requirements.txt
