import pandas as pd
import joblib

from sklearn.metrics.pairwise import cosine_similarity


DATA_FILE = "data/medquad.csv"
VECTORIZER_FILE = "models/tfidf_vectorizer.pkl"
MATRIX_FILE = "models/tfidf_matrix.pkl"


# Load dataset and saved models
df = pd.read_csv(DATA_FILE)

vectorizer = joblib.load(VECTORIZER_FILE)
tfidf_matrix = joblib.load(MATRIX_FILE)


def ask_question(user_question, threshold=0.50):

    # Convert user's question into TF-IDF vector
    question_vector = vectorizer.transform([user_question])

    # Calculate similarity with every MedQuAD question
    similarities = cosine_similarity(
        question_vector,
        tfidf_matrix
    ).flatten()

    # Find the most similar question
    best_index = similarities.argmax()

    best_score = similarities[best_index]

    # Get matching record
    result = df.iloc[best_index]

    # Check similarity threshold
    if best_score < threshold:

        return {
            "found": False,
            "answer": "I could not find a sufficiently relevant medical answer in the MedQuAD knowledge base.",
            "question": "",
            "question_type": "",
            "focus": "",
            "score": float(best_score)
        }

    return {
        "found": True,
        "answer": result["answer"],
        "question": result["question"],
        "question_type": result["question_type"],
        "focus": result["focus"],
        "score": float(best_score)
    }


if __name__ == "__main__":

    print("Medical Q&A Retrieval System")
    print("============================")

    question = input("\nEnter your medical question: ")

    result = ask_question(question)

    print("\n--------------------------------")
    print("RESULT")
    print("--------------------------------")

    print("Matched Question:")
    print(result["question"])

    print("\nQuestion Type:")
    print(result["question_type"])

    print("\nMedical Focus:")
    print(result["focus"])

    print("\nSimilarity Score:")
    print(f"{result['score']:.2%}")

    print("\nAnswer:")
    print(result["answer"])