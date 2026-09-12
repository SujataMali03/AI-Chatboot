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

TOP_K = 5


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

print("Embedding model loaded.")


# ============================================================
# CONNECT TO CHROMADB
# ============================================================

print("Connecting to ChromaDB...")

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
# SEARCH PAPERS
# ============================================================

def search_papers(question, top_k=TOP_K):

    # Convert question to embedding
    query_embedding = embedding_model.encode(
        [question]
    )[0].tolist()

    # Search database
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


# ============================================================
# BUILD RESEARCH CONTEXT
# ============================================================

def build_context(results):

    context_parts = []

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    for i, document in enumerate(documents):

        title = metadatas[i]["title"]

        authors = metadatas[i]["authors"]

        categories = metadatas[i]["categories"]

        paper_context = f"""
Research Paper {i + 1}

Title:
{title}

Authors:
{authors}

Categories:
{categories}

Content:
{document}
"""

        context_parts.append(
            paper_context
        )

    return "\n".join(context_parts)


# ============================================================
# GENERATE ANSWER USING LLAMA 3
# ============================================================

def generate_answer(question, context):

    prompt = f"""
You are an expert scientific research assistant
specialized in Computer Science.

Your job is to answer the user's question using
the research papers provided below.

IMPORTANT RULES:

1. Use the provided research context.
2. Give accurate and understandable explanations.
3. Explain complex concepts step-by-step.
4. Do not invent research papers or citations.
5. If the provided papers do not contain enough
   information, clearly say so.
6. Mention relevant paper titles when useful.
7. Distinguish between information from the papers
   and general explanation.
8. Do not claim that a paper proves something unless
   the provided context supports it.

RESEARCH PAPERS:

{context}

USER QUESTION:

{question}

Now provide a clear scientific answer.
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
    distances = results["distances"][0]

    for i, metadata in enumerate(metadatas):

        print(f"\n[{i + 1}] {metadata['title']}")

        print(
            f"Categories: "
            f"{metadata['categories']}"
        )

        print(
            f"Distance: "
            f"{distances[i]:.4f}"
        )


# ============================================================
# MAIN CHAT LOOP
# ============================================================

print("\n" + "=" * 70)
print("SCIENTIFIC RESEARCH RAG CHATBOT")
print("=" * 70)

print("Ask questions about Computer Science research.")

print("Type 'exit' to stop.")

while True:

    question = input("\nYou: ")

    if question.lower().strip() == "exit":

        print("\nGoodbye!")

        break

    if not question.strip():

        print("Please enter a question.")

        continue

    print("\nSearching research papers...")

    results = search_papers(
        question,
        TOP_K
    )

    print(
        f"Retrieved "
        f"{len(results['ids'][0])} papers."
    )

    print("\nGenerating answer with Llama 3...")

    context = build_context(
        results
    )

    answer = generate_answer(
        question,
        context
    )

    print("\n" + "=" * 70)
    print("SCIENTIFIC ANSWER")
    print("=" * 70)

    print(answer)

    display_sources(results)