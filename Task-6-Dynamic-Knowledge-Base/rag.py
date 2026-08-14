import os
import chromadb
from dotenv import load_dotenv
from google import genai

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found. Please check your .env file."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=API_KEY
)


# ============================================================
# CHROMADB CONNECTION
# ============================================================

db_client = chromadb.PersistentClient(
    path="vector_db"
)

collection = db_client.get_or_create_collection(
    name="knowledge_base"
)


# ============================================================
# CREATE EMBEDDING
# ============================================================

def create_embedding(text):
    """
    Convert text into a vector embedding.
    """

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return result.embeddings[0].values


# ============================================================
# SEARCH KNOWLEDGE BASE
# ============================================================

def search_knowledge(question):
    """
    Search ChromaDB for information relevant
    to the user's question.
    """

    # Check if database is empty
    total_documents = collection.count()

    if total_documents == 0:
        return []

    # Create embedding for user's question
    query_embedding = create_embedding(question)

    # Number of results
    number_of_results = min(3, total_documents)

    # Search vector database
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=number_of_results
    )

    documents = results.get("documents", [])

    if not documents:
        return []

    return documents[0]


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(question):
    """
    Retrieve relevant information from the knowledge base
    and generate an answer using Gemini.
    """

    # Search knowledge base
    documents = search_knowledge(question)

    # If no information exists
    if not documents:
        return (
            "The knowledge base is currently empty. "
            "Please update the knowledge base first."
        )

    # Combine retrieved documents
    context = "\n\n".join(documents)

    # Prompt for Gemini
    prompt = f"""
You are a helpful knowledge-base chatbot.

Your task is to answer the user's question using
ONLY the information provided in the context.

================ CONTEXT ================

{context}

============== END CONTEXT ==============

User Question:
{question}

Instructions:

1. Answer clearly and simply.
2. Use only information from the context.
3. Do not invent or assume information.
4. If the answer is not available in the context,
   say:

   "I don't have this information in my knowledge base."

5. Keep the answer relevant to the user's question.

Answer:
"""

    # Generate response
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


# ============================================================
# TEST THE RAG SYSTEM
# ============================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print(" Dynamic Knowledge Base RAG Chatbot")
    print("==========================================")
    print()

    print(
        "Documents in vector database:",
        collection.count()
    )

    print()

    question = input(
        "Enter your question: "
    )

    if question.strip():

        print()
        print("Searching knowledge base...")
        print()

        try:

            answer = generate_answer(question)

            print("Answer:")
            print("------------------------------------------")
            print(answer)
            print("------------------------------------------")

        except Exception as e:

            print()
            print("Error:")
            print(e)

    else:

        print("Please enter a question.")