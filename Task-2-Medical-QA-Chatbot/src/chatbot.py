from qa_engine import ask_question
from entity_recognition import find_entities, detect_question_type


def medical_chatbot(user_question):

    # Entity recognition
    entities = find_entities(user_question)

    # Detect question type
    question_type = detect_question_type(user_question)

    # Retrieve answer
    result = ask_question(user_question)

    return {
        "entities": entities,
        "question_type": question_type,
        "retrieval": result
    }


if __name__ == "__main__":

    print("======================================")
    print("       MEDICAL Q&A CHATBOT")
    print("======================================")

    question = input("\nAsk your medical question: ")

    response = medical_chatbot(question)

    print("\nMedical Entities")
    print("----------------")
    print("Diseases:", response["entities"]["diseases"])
    print("Symptoms:", response["entities"]["symptoms"])
    print("Treatments:", response["entities"]["treatments"])

    print("\nDetected Question Type:")
    print(response["question_type"])

    print("\nRetrieved Question:")
    print(response["retrieval"]["question"])

    print("\nSimilarity Score:")
    print(f"{response['retrieval']['score']:.2%}")

    print("\nAnswer")
    print("----------------")
    print(response["retrieval"]["answer"])

    print("\n⚠️ Educational information only.")
    print("Consult a qualified healthcare professional for medical advice.")