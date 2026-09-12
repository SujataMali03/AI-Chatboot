import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

CHROMA_PATH = "database/chroma_db"

COLLECTION_NAME = "arxiv_cs_papers"

TOP_K = 5


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

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

print(f"Database contains {collection.count():,} papers.")


# ============================================================
# SEARCH FUNCTION
# ============================================================

def search_papers(query, top_k=TOP_K):

    # Convert user's question into an embedding
    query_embedding = model.encode(
        [query]
    )[0].tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


# ============================================================
# INTERACTIVE SEARCH
# ============================================================

print("\n" + "=" * 60)
print("SCIENTIFIC PAPER SEARCH")
print("=" * 60)

print("Type 'exit' to quit.")

while True:

    query = input("\nEnter your research question: ")

    if query.lower() == "exit":
        print("Goodbye!")
        break

    if not query.strip():
        print("Please enter a question.")
        continue

    results = search_papers(query)

    print("\n" + "=" * 60)
    print("MOST RELEVANT PAPERS")
    print("=" * 60)

    for i in range(len(results["ids"][0])):

        paper_id = results["ids"][0][i]

        document = results["documents"][0][i]

        metadata = results["metadatas"][0][i]

        distance = results["distances"][0][i]

        print(f"\n{'-' * 60}")

        print(f"Result #{i + 1}")

        print(f"Paper ID: {paper_id}")

        print(f"Title: {metadata['title']}")

        print(f"Authors: {metadata['authors']}")

        print(f"Categories: {metadata['categories']}")

        print(f"Distance: {distance:.4f}")

        print("\nAbstract:")

        # Extract abstract from stored document
        if "Abstract:" in document:

            abstract = document.split(
                "Abstract:",
                1
            )[1]

            if "Categories:" in abstract:

                abstract = abstract.split(
                    "Categories:",
                    1
                )[0]

            print(abstract.strip())

        else:

            print(document)