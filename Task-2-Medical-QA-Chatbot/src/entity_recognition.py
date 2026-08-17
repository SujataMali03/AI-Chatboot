import re


# Common medical diseases/conditions
DISEASES = [
    "diabetes",
    "diabetes mellitus",
    "asthma",
    "cancer",
    "hypertension",
    "influenza",
    "pneumonia",
    "leukemia",
    "adult acute lymphoblastic leukemia",
    "acute lymphoblastic leukemia",
    "obesity",
    "arthritis",
    "malaria",
    "tuberculosis",
    "slipped capital femoral epiphysis",
    "hip osteoarthritis",
    "proximial femoral epiphysiolysis",
]


# Common symptoms
SYMPTOMS = [
    "fever",
    "cough",
    "headache",
    "fatigue",
    "tired",
    "weakness",
    "pain",
    "shortness of breath",
    "weight loss",
    "night sweats",
    "bleeding",
    "bruising",
    "nausea",
    "vomiting",
    "loss of appetite",
    "hip pain",
    "difficulty walking",
]


# Common treatments
TREATMENTS = [
    "chemotherapy",
    "radiation therapy",
    "radiation",
    "surgery",
    "medication",
    "therapy",
    "stem cell transplant",
    "targeted therapy",
    "immunotherapy",
]


def contains_term(text, term):

    text = text.lower()
    term = term.lower()

    return re.search(
        r"\b" + re.escape(term) + r"\b",
        text
    ) is not None


def find_entities(text):

    entities = {
        "diseases": [],
        "symptoms": [],
        "treatments": []
    }

    # Disease detection
    for disease in DISEASES:
        if contains_term(text, disease):
            entities["diseases"].append(disease)

    # Symptom detection
    for symptom in SYMPTOMS:
        if contains_term(text, symptom):
            entities["symptoms"].append(symptom)

    # Treatment detection
    for treatment in TREATMENTS:
        if contains_term(text, treatment):
            entities["treatments"].append(treatment)

    return entities


def detect_question_type(text):

    text_lower = text.lower()

    # Symptoms
    if any(word in text_lower for word in [
        "symptom",
        "symptoms",
        "sign",
        "signs",
        "feel",
        "indications"
    ]):
        return "Symptoms"

    # Treatment
    if any(word in text_lower for word in [
        "treatment",
        "treatments",
        "treat",
        "therapy",
        "therapies",
        "medicine",
        "medication",
        "medications",
        "cure"
    ]):
        return "Treatment"

    # Causes
    if any(word in text_lower for word in [
        "cause",
        "causes",
        "why",
        "reason"
    ]):
        return "Causes"

    # Diagnosis
    if any(word in text_lower for word in [
        "diagnose",
        "diagnosis",
        "test",
        "tests",
        "testing",
        "diagnostic"
    ]):
        return "Diagnosis"

    # Prevention
    if any(word in text_lower for word in [
        "prevent",
        "prevention",
        "avoid"
    ]):
        return "Prevention"

    return "General Information"


if __name__ == "__main__":

    question = input("Enter a medical question: ")

    entities = find_entities(question)

    question_type = detect_question_type(question)

    print("\nMedical Entities")
    print("================")

    print("Diseases:", entities["diseases"])
    print("Symptoms:", entities["symptoms"])
    print("Treatments:", entities["treatments"])

    print("\nQuestion Type:", question_type)