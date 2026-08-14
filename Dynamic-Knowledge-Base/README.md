\# 🤖 Dynamic Knowledge Base Chatbot



\## Project Overview



This project implements a Dynamic Knowledge Base Chatbot using Retrieval-Augmented Generation (RAG).



The chatbot can automatically incorporate new information into its knowledge base without retraining the language model.



New information is collected from specified source files, converted into vector embeddings, and stored in a ChromaDB vector database.



When a user asks a question, the chatbot retrieves relevant information from the vector database and uses Google Gemini to generate an answer.



\---



\## Objectives



The main objectives of this project are:



\- Build a chatbot using RAG.

\- Store knowledge in a vector database.

\- Detect changes in knowledge sources.

\- Automatically update the vector database.

\- Retrieve relevant information for user questions.

\- Generate answers using Google Gemini.

\- Provide a simple Streamlit interface.

\- Periodically check for new information.



\---



\## Technologies Used



\- Python

\- Streamlit

\- Google Gemini API

\- Google GenAI SDK

\- ChromaDB

\- Retrieval-Augmented Generation (RAG)

\- Python-dotenv

\- Schedule

\- Vector Embeddings



\---



\## Project Structure



```text

dynamic\_chatbot/

│

├── app.py

├── rag.py

├── updater.py

├── scheduler.py

├── requirements.txt

├── README.md

├── .env

├── .gitignore

│

├── sources/

│   └── knowledge.txt

│

├── data/

│   └── source\_state.json

│

├── vector\_db/

│

└── venv/

