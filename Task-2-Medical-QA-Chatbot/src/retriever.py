import pandas as pd
import re
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DATA_FILE = "data/medquad.csv"
VECTORIZER_FILE = "models/tfidf_vectorizer.pkl"
MATRIX_FILE = "models/tfidf_matrix.pkl"


def clean_text(text):
    """Clean text for retrieval."""
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_retrieval_index():

    print("Loading MedQuAD dataset...")

    df = pd.read_csv(DATA_FILE)

    # Remove records with missing questions or answers
    df = df.dropna(subset=["question", "answer"])

    # Clean questions
    df["clean_question"] = df["question"].apply(clean_text)

    print(f"Loaded {len(df)} question-answer pairs.")

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=50000
    )

    # Convert questions into TF-IDF vectors
    tfidf_matrix = vectorizer.fit_transform(df["clean_question"])

    # Save everything
    joblib.dump(vectorizer, VECTORIZER_FILE)
    joblib.dump(tfidf_matrix, MATRIX_FILE)

    # Save cleaned dataset
    df.to_csv(DATA_FILE, index=False)

    print()
    print("======================================")
    print("Retrieval index created successfully!")
    print("======================================")
    print(f"Questions indexed: {len(df)}")
    print(f"Vectorizer: {VECTORIZER_FILE}")
    print(f"TF-IDF matrix: {MATRIX_FILE}")


if __name__ == "__main__":
    build_retrieval_index()