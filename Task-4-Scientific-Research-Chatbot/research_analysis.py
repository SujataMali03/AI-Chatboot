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

print("=" * 60)
print("SCIENTIFIC RESEARCH ANALYSIS")
print("=" * 60)

print("\nLoading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

print("Embedding model loaded successfully.")


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
    f"Database connected. "
    f"Papers available: {collection.count():,}"
)


# ============================================================
# SEARCH PAPERS
# ============================================================

def search_papers(query, top_k=TOP_K):

    query_embedding = embedding_model.encode(
        [query]
    )[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


# ============================================================
# CREATE RESEARCH CONTEXT
# ============================================================

def build_context(results):

    context = ""

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for i in range(len(documents)):

        context += f"""

================ PAPER {i + 1} ================

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
# RESEARCH ANALYSIS WITH LLAMA 3
# ============================================================

def analyze_research(query, context):

    prompt = f"""
You are an expert Computer Science research assistant.

Analyze the research papers provided below and answer
the user's request using the available research context.

USER REQUEST:
{query}

RESEARCH PAPERS:
{context}

Provide the answer using the following structure:

1. Research Topic
2. Short Summary
3. Research Problem
4. Proposed Approach / Methodology
5. Key Findings
6. Important Concepts
7. Applications
8. Limitations or Challenges
9. Overall Conclusion

IMPORTANT RULES:

- Use the provided papers as the main source.
- Do not invent facts or research results.
- If information is not available, say "Not specified in the provided papers."
- Explain technical concepts in simple language where possible.
- Mention relevant paper titles when appropriate.
- Keep the response organized and readable.
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

    print("\n" + "=" * 60)
    print("SOURCE PAPERS")
    print("=" * 60)

    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, metadata in enumerate(metadatas):

        print(f"\n[{i + 1}] {metadata['title']}")

        print(
            f"Authors: {metadata['authors']}"
        )

        print(
            f"Categories: {metadata['categories']}"
        )

        print(
            f"Similarity distance: "
            f"{distances[i]:.4f}"
        )


# ============================================================
# MAIN PROGRAM
# ============================================================

while True:

    print("\n" + "-" * 60)

    query = input(
        "Enter a research topic or question "
        "(type 'exit' to quit): "
    )

    if query.lower().strip() == "exit":

        print("\nExiting research analysis.")

        break

    if not query.strip():

        print("Please enter a valid query.")

        continue

    print("\nSearching relevant research papers...")

    results = search_papers(
        query,
        TOP_K
    )

    print(
        f"Retrieved {len(results['ids'][0])} research papers."
    )

    print("\nAnalyzing papers with Llama 3...")

    context = build_context(results)

    answer = analyze_research(
        query,
        context
    )

    print("\n" + "=" * 60)
    print("RESEARCH ANALYSIS")
    print("=" * 60)

    print(answer)

    display_sources(results)