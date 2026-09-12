import chromadb
import ollama
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

CHROMA_PATH = "database/chroma_db"
COLLECTION_NAME = "arxiv_cs_papers"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "llama3:latest"

TOP_K = 3


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("=" * 70)
print("SCIENTIFIC RESEARCH CHATBOT")
print("=" * 70)

print("\nLoading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

print("Embedding model loaded.")


# ============================================================
# CONNECT TO CHROMADB
# ============================================================

print("\nConnecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

print(
    f"Connected successfully. "
    f"Papers available: {collection.count():,}"
)


# ============================================================
# CONVERSATION MEMORY
# ============================================================

conversation_history = []


# ============================================================
# SEARCH PAPERS
# ============================================================

def search_papers(question):

    query_embedding = embedding_model.encode(
        [question]
    )[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K
    )

    return results


# ============================================================
# BUILD PAPER CONTEXT
# ============================================================

def build_context(results):

    context = ""

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for i in range(len(documents)):

        context += f"""

--- Research Paper {i + 1} ---

Title:
{metadatas[i]["title"]}

Authors:
{metadatas[i]["authors"]}

Categories:
{metadatas[i]["categories"]}

Abstract:
{documents[i]}

"""

    return context


# ============================================================
# BUILD CONVERSATION HISTORY
# ============================================================

def build_history():

    if not conversation_history:
        return "No previous conversation."

    history = ""

    for item in conversation_history[-6:]:

        history += f"""
User:
{item["user"]}

Assistant:
{item["assistant"]}

"""

    return history


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(question, context):

    history = build_history()

    prompt = f"""
You are an expert Computer Science research assistant.

You are having a continuous conversation with the user.

IMPORTANT:

- Remember the previous conversation.
- Understand follow-up questions.
- Resolve words such as "it", "this", "that", "they",
  and "the above concept" using previous conversation.
- Use the research papers as supporting context.
- Give clear and technically accurate explanations.
- Explain difficult concepts step-by-step.
- Do not invent research findings.
- If the papers do not contain enough information,
  clearly state that.
- You may use general scientific knowledge for explanation,
  but do not pretend it came from the research papers.

============================================================
PREVIOUS CONVERSATION
============================================================

{history}

============================================================
RESEARCH PAPERS
============================================================

{context}

============================================================
CURRENT USER QUESTION
============================================================

{question}

============================================================

Answer the current question while maintaining continuity
with the previous conversation.
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# ============================================================
# DISPLAY SOURCES
# ============================================================

def display_sources(results):

    print("\n" + "=" * 70)
    print("RESEARCH SOURCES")
    print("=" * 70)

    metadatas = results["metadatas"][0]

    for i, metadata in enumerate(metadatas):

        print(
            f"\n[{i + 1}] {metadata['title']}"
        )

        print(
            f"Categories: {metadata['categories']}"
        )


# ============================================================
# CHAT LOOP
# ============================================================

print("\n" + "=" * 70)
print("FOLLOW-UP CHAT ENABLED")
print("=" * 70)

print("The chatbot now remembers the current conversation.")

print("\nCommands:")
print("  exit  - quit")
print("  clear - clear conversation memory")


while True:

    question = input("\nYou: ").strip()

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    if question.lower() == "exit":

        print("\nGoodbye!")

        break


    # --------------------------------------------------------
    # CLEAR MEMORY
    # --------------------------------------------------------

    if question.lower() == "clear":

        conversation_history.clear()

        print("\nConversation memory cleared.")

        continue


    # --------------------------------------------------------
    # EMPTY INPUT
    # --------------------------------------------------------

    if not question:

        print("Please enter a question.")

        continue


    # --------------------------------------------------------
    # RETRIEVE PAPERS
    # --------------------------------------------------------

    print("\nSearching research papers...")

    results = search_papers(
        question
    )

    print(
        f"Retrieved {len(results['ids'][0])} papers."
    )


    # --------------------------------------------------------
    # GENERATE ANSWER
    # --------------------------------------------------------

    print("Generating response with Llama 3...")

    context = build_context(
        results
    )

    answer = generate_answer(
        question,
        context
    )


    # --------------------------------------------------------
    # SAVE CONVERSATION
    # --------------------------------------------------------

    conversation_history.append(
        {
            "user": question,
            "assistant": answer
        }
    )


    # --------------------------------------------------------
    # DISPLAY ANSWER
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("SCIENTIFIC ASSISTANT")
    print("=" * 70)

    print(answer)


    # --------------------------------------------------------
    # DISPLAY SOURCES
    # --------------------------------------------------------

    display_sources(
        results
    )