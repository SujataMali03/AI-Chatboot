\# Task 4 - Scientific Research Chatbot



\## Project Overview



The Scientific Research Chatbot is an AI-powered research assistant developed using the arXiv dataset. It focuses on Computer Science research papers and helps users search papers, understand advanced concepts, summarize research, extract important information, and ask follow-up questions.



The project uses Retrieval-Augmented Generation (RAG) with an open-source Llama 3 model to generate research-based explanations.



\## Objective



To develop a chatbot that can:



\- Answer complex scientific and technical questions

\- Search relevant research papers

\- Explain advanced Computer Science concepts

\- Summarize research papers

\- Extract important information from papers

\- Support follow-up questions

\- Visualize important concepts



\## Dataset



The project uses the arXiv scientific research dataset from Kaggle.



A Computer Science subset of the dataset is used for this project.



\## Technologies Used



\- Python

\- Streamlit

\- Sentence Transformers

\- ChromaDB

\- Ollama

\- Llama 3

\- Pandas

\- NumPy

\- Retrieval-Augmented Generation (RAG)



\## System Architecture



```text

arXiv Dataset

&#x20;     ↓

Computer Science Papers

&#x20;     ↓

Data Cleaning \& Preprocessing

&#x20;     ↓

Sentence Transformer Embeddings

&#x20;     ↓

ChromaDB Vector Database

&#x20;     ↓

User Query

&#x20;     ↓

Semantic Search / Retrieval

&#x20;     ↓

Relevant Research Context

&#x20;     ↓

Llama 3 through Ollama

&#x20;     ↓

Generated Explanation

&#x20;     ↓

Streamlit Interface

