import os
import json
import hashlib
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
# PATHS
# ============================================================

DB_PATH = "vector_db"

STATE_FILE = os.path.join(
    "data",
    "source_state.json"
)

SOURCE_FOLDER = "sources"


# ============================================================
# CREATE REQUIRED FOLDERS
# ============================================================

os.makedirs("data", exist_ok=True)

os.makedirs(
    "vector_db",
    exist_ok=True
)

os.makedirs(
    "sources",
    exist_ok=True
)


# ============================================================
# CHROMADB
# ============================================================

db_client = chromadb.PersistentClient(
    path=DB_PATH
)

collection = db_client.get_or_create_collection(
    name="knowledge_base"
)


# ============================================================
# FILE HASH
# ============================================================

def get_file_hash(filepath):
    """
    Generate a unique hash for a file.

    If the file changes, its hash also changes.
    This allows us to detect new information.
    """

    with open(filepath, "rb") as file:

        file_data = file.read()

    return hashlib.md5(
        file_data
    ).hexdigest()


# ============================================================
# LOAD PREVIOUS FILE INFORMATION
# ============================================================

def load_state():

    if not os.path.exists(STATE_FILE):

        return {}

    with open(
        STATE_FILE,
        "r"
    ) as file:

        return json.load(file)


# ============================================================
# SAVE FILE INFORMATION
# ============================================================

def save_state(state):

    with open(
        STATE_FILE,
        "w"
    ) as file:

        json.dump(
            state,
            file,
            indent=4
        )


# ============================================================
# SPLIT TEXT INTO CHUNKS
# ============================================================

def create_chunks(
    text,
    chunk_size=500
):
    """
    Split large text into smaller pieces.
    """

    words = text.split()

    chunks = []

    for i in range(
        0,
        len(words),
        chunk_size
    ):

        chunk = " ".join(
            words[
                i:i + chunk_size
            ]
        )

        if chunk.strip():

            chunks.append(chunk)

    return chunks


# ============================================================
# CREATE EMBEDDING
# ============================================================

def create_embedding(text):

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return result.embeddings[0].values


# ============================================================
# UPDATE KNOWLEDGE BASE
# ============================================================

def update_knowledge_base():

    print()
    print("==========================================")
    print(" Checking Knowledge Sources")
    print("==========================================")
    print()

    # Load previous state
    state = load_state()

    files_found = 0

    files_updated = 0

    # Get all files from sources folder
    for filename in os.listdir(
        SOURCE_FOLDER
    ):

        filepath = os.path.join(
            SOURCE_FOLDER,
            filename
        )

        # Ignore folders
        if not os.path.isfile(filepath):

            continue

        # Currently process TXT files
        if not filename.lower().endswith(".txt"):

            continue

        files_found += 1

        print(
            f"Checking: {filename}"
        )

        # Generate current hash
        current_hash = get_file_hash(
            filepath
        )

        # Get previous hash
        old_hash = state.get(
            filepath
        )

        # Check if file is unchanged
        if current_hash == old_hash:

            print(
                f"No changes detected: {filename}"
            )

            continue

        print(
            f"New or updated information found: {filename}"
        )

        # Read source file
        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        # Split into chunks
        chunks = create_chunks(
            text
        )

        print(
            f"Created {len(chunks)} chunks."
        )

        # Create embeddings
        for index, chunk in enumerate(
            chunks
        ):

            try:

                embedding = create_embedding(
                    chunk
                )

                document_id = (
                    f"{filename}_"
                    f"{current_hash}_"
                    f"{index}"
                )

                collection.upsert(

                    ids=[
                        document_id
                    ],

                    documents=[
                        chunk
                    ],

                    embeddings=[
                        embedding
                    ]
                )

                print(
                    f"Added chunk {index + 1}"
                )

            except Exception as error:

                print(
                    f"Error processing chunk "
                    f"{index + 1}: {error}"
                )

        # Save new hash
        state[filepath] = current_hash

        files_updated += 1

        print(
            f"Successfully updated: {filename}"
        )

        print()

    # Save state
    save_state(state)

    print()
    print("==========================================")
    print(" Knowledge Base Update Completed")
    print("==========================================")

    print(
        f"Files found: {files_found}"
    )

    print(
        f"Files updated: {files_updated}"
    )

    print(
        f"Documents in database: "
        f"{collection.count()}"
    )

    print(
        "=========================================="
    )

    print()


# ============================================================
# RUN UPDATE
# ============================================================

if __name__ == "__main__":

    update_knowledge_base()