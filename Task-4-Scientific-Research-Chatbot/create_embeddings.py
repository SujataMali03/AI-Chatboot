import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "data/cs_papers_clean.csv"

CHROMA_PATH = "database/chroma_db"

COLLECTION_NAME = "arxiv_cs_papers"

# ChromaDB maximum in your installation is 5461.
# We use 5000 to stay safely below the limit.
BATCH_SIZE = 5000


# ============================================================
# STEP 1 — LOAD DATASET
# ============================================================

print("=" * 60)
print("STEP 1: Loading cleaned arXiv papers")
print("=" * 60)

df = pd.read_csv(INPUT_FILE)

print(f"Total papers loaded: {len(df):,}")


# ============================================================
# STEP 2 — LOAD EMBEDDING MODEL
# ============================================================

print("\n" + "=" * 60)
print("STEP 2: Loading embedding model")
print("=" * 60)

print("Model: all-MiniLM-L6-v2")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded successfully.")


# ============================================================
# STEP 3 — CREATE CHROMADB
# ============================================================

print("\n" + "=" * 60)
print("STEP 3: Creating ChromaDB")
print("=" * 60)

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

print("ChromaDB collection ready.")

existing_count = collection.count()

print(f"Existing papers in database: {existing_count:,}")


# ============================================================
# STEP 4 — PREPARE DOCUMENTS
# ============================================================

print("\n" + "=" * 60)
print("STEP 4: Preparing research papers")
print("=" * 60)

documents = []

for _, row in df.iterrows():

    title = str(row["title"])
    abstract = str(row["abstract"])
    categories = str(row["categories"])

    document = (
        "Title: " + title +
        "\n\nAbstract: " + abstract +
        "\n\nCategories: " + categories
    )

    documents.append(document)

print(f"Documents prepared: {len(documents):,}")


# ============================================================
# STEP 5 — CREATE EMBEDDINGS
# ============================================================

print("\n" + "=" * 60)
print("STEP 5: Generating embeddings")
print("=" * 60)

print("This may take several minutes...")

embeddings = model.encode(
    documents,
    batch_size=32,
    show_progress_bar=True
)

print("\nEmbeddings generated successfully.")


# ============================================================
# STEP 6 — PREPARE IDS AND METADATA
# ============================================================

print("\n" + "=" * 60)
print("STEP 6: Preparing metadata")
print("=" * 60)

ids = df["id"].astype(str).tolist()

metadatas = []

for _, row in df.iterrows():

    metadata = {
        "title": str(row["title"]),
        "authors": str(row["authors"]),
        "categories": str(row["categories"]),
        "update_date": str(row["update_date"])
    }

    metadatas.append(metadata)

print(f"Metadata prepared: {len(metadatas):,}")


# ============================================================
# STEP 7 — STORE EMBEDDINGS IN BATCHES
# ============================================================

print("\n" + "=" * 60)
print("STEP 7: Storing embeddings in ChromaDB")
print("=" * 60)

print(f"Batch size: {BATCH_SIZE:,}")

total_records = len(ids)

for start in range(0, total_records, BATCH_SIZE):

    end = min(start + BATCH_SIZE, total_records)

    batch_ids = ids[start:end]

    batch_documents = documents[start:end]

    batch_embeddings = embeddings[start:end].tolist()

    batch_metadatas = metadatas[start:end]

    print(
        f"\nAdding papers "
        f"{start + 1:,} - {end:,} "
        f"out of {total_records:,}"
    )

    # --------------------------------------------------------
    # Check whether IDs already exist
    # --------------------------------------------------------

    existing = collection.get(
        ids=batch_ids,
        include=[]
    )

    existing_ids = set(existing["ids"])

    # Keep only new records
    new_indices = [
        i
        for i, paper_id in enumerate(batch_ids)
        if paper_id not in existing_ids
    ]

    if not new_indices:

        print("All papers in this batch already exist. Skipping.")

        continue

    new_ids = [
        batch_ids[i]
        for i in new_indices
    ]

    new_documents = [
        batch_documents[i]
        for i in new_indices
    ]

    new_embeddings = [
        batch_embeddings[i]
        for i in new_indices
    ]

    new_metadatas = [
        batch_metadatas[i]
        for i in new_indices
    ]

    collection.add(
        ids=new_ids,
        documents=new_documents,
        embeddings=new_embeddings,
        metadatas=new_metadatas
    )

    print(
        f"Added {len(new_ids):,} new papers."
    )


# ============================================================
# STEP 8 — FINAL RESULT
# ============================================================

final_count = collection.count()

print("\n")
print("=" * 60)
print("EMBEDDING PROCESS COMPLETED SUCCESSFULLY!")
print("=" * 60)

print(f"Total papers in dataset : {total_records:,}")
print(f"Papers in ChromaDB      : {final_count:,}")
print(f"Database location       : {CHROMA_PATH}")
print(f"Collection name         : {COLLECTION_NAME}")

print("=" * 60)