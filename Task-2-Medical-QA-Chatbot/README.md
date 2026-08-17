\# 🩺 Medical Q\&A Chatbot



A specialized \*\*Medical Question-Answering Chatbot\*\* developed using the \*\*MedQuAD dataset\*\*. The system retrieves relevant medical answers based on user questions using \*\*TF-IDF vectorization and Cosine Similarity\*\*. It also performs basic medical entity recognition and provides an interactive web interface using \*\*Streamlit\*\*.



\---



\## 📌 Project Overview



The Medical Q\&A Chatbot is designed to answer medical questions using information available in the MedQuAD dataset.



Instead of generating answers from an external Large Language Model, this project uses a \*\*retrieval-based approach\*\*. The user's question is compared with medical questions in the MedQuAD knowledge base, and the most relevant question-answer pair is retrieved.



The system also identifies basic medical entities such as:



\* Diseases

\* Symptoms

\* Treatments



It classifies questions into categories such as:



\* Symptoms

\* Treatment

\* Causes

\* Diagnosis

\* Prevention

\* General Information



A relevance threshold is used to prevent the chatbot from returning unrelated medical answers for non-medical questions.



\---



\# 🎯 Objectives



The main objectives of this project are:



1\. To develop a specialized medical question-answering chatbot.

2\. To use the MedQuAD dataset as the medical knowledge base.

3\. To preprocess and convert the MedQuAD XML dataset into a structured CSV file.

4\. To implement a retrieval mechanism using TF-IDF.

5\. To use Cosine Similarity to identify relevant medical questions.

6\. To implement basic medical entity recognition.

7\. To classify the user's medical question.

8\. To provide a simple and interactive Streamlit interface.

9\. To reject questions that are not sufficiently relevant to the medical knowledge base.

10\. To provide educational medical information with an appropriate disclaimer.



\---



\# 📚 Dataset



\## MedQuAD Dataset



This project uses the \*\*MedQuAD (Medical Question Answering Dataset)\*\*.



The dataset contains medical question-answer pairs collected from reliable health-related sources.



Dataset repository:



\*\*MedQuAD GitHub Repository:\*\*

https://github.com/abachaa/MedQuAD



The downloaded dataset contains multiple categories/folders, including sources such as:



\* CancerGov

\* GARD

\* GHR

\* MedlinePlus Health Topics

\* NIDDK

\* NINDS

\* SeniorHealth

\* NHLBI

\* CDC

\* MedlinePlus ADAM

\* MedlinePlus Drugs

\* MedlinePlus Herbs and Supplements



The original dataset is provided by its respective authors and is subject to its own license and terms of use.



\---



\# 🏗️ System Architecture



```text

&#x20;               ┌──────────────────────┐

&#x20;               │    MedQuAD Dataset   │

&#x20;               │       XML Files      │

&#x20;               └──────────┬───────────┘

&#x20;                          │

&#x20;                          ▼

&#x20;               ┌──────────────────────┐

&#x20;               │  Data Preprocessing  │

&#x20;               │      XML → CSV       │

&#x20;               └──────────┬───────────┘

&#x20;                          │

&#x20;                          ▼

&#x20;               ┌──────────────────────┐

&#x20;               │   TF-IDF Vectorizer  │

&#x20;               └──────────┬───────────┘

&#x20;                          │

&#x20;                          ▼

User Question ──────► Streamlit UI

&#x20;                          │

&#x20;                          ▼

&#x20;               ┌──────────────────────┐

&#x20;               │ Medical Entity       │

&#x20;               │ Recognition          │

&#x20;               └──────────┬───────────┘

&#x20;                          │

&#x20;                          ▼

&#x20;               ┌──────────────────────┐

&#x20;               │ Question Type        │

&#x20;               │ Detection             │

&#x20;               └──────────┬───────────┘

&#x20;                          │

&#x20;                          ▼

&#x20;               ┌──────────────────────┐

&#x20;               │ TF-IDF Question      │

&#x20;               │ Vector               │

&#x20;               └──────────┬───────────┘

&#x20;                          │

&#x20;                          ▼

&#x20;               ┌──────────────────────┐

&#x20;               │ Cosine Similarity    │

&#x20;               └──────────┬───────────┘

&#x20;                          │

&#x20;                          ▼

&#x20;               ┌──────────────────────┐

&#x20;               │ Relevance Threshold  │

&#x20;               └──────────┬───────────┘

&#x20;                          │

&#x20;                ┌─────────┴─────────┐

&#x20;                │                   │

&#x20;            Relevant            Not Relevant

&#x20;                │                   │

&#x20;                ▼                   ▼

&#x20;       MedQuAD Answer          Rejection Message

&#x20;                │

&#x20;                ▼

&#x20;         Streamlit Response

```



\---



\# 🔄 Working Process



The chatbot works through the following steps:



\### Step 1 — Dataset Collection



The MedQuAD dataset is downloaded and stored inside the project.



\### Step 2 — Data Preprocessing



The XML files are automatically scanned and important information is extracted, including:



\* Document ID

\* Question ID

\* Question

\* Answer

\* Question Type

\* Medical Focus

\* Source

\* URL



The extracted information is stored in:



```text

data/medquad.csv

```



\### Step 3 — TF-IDF Vectorization



The questions from the MedQuAD dataset are converted into numerical vectors using \*\*TF-IDF (Term Frequency-Inverse Document Frequency)\*\*.



\### Step 4 — User Question Processing



When the user enters a question, the question is also converted into a TF-IDF vector.



\### Step 5 — Similarity Calculation



Cosine Similarity is calculated between the user's question and the questions stored in the MedQuAD dataset.



\### Step 6 — Best Match Retrieval



The question with the highest similarity score is selected.



\### Step 7 — Relevance Filtering



A similarity threshold is applied.



The current threshold is:



```text

50%

```



If the similarity is below the threshold, the chatbot does not return the retrieved answer.



Instead, it displays:



```text

I could not find a sufficiently relevant medical

answer in the MedQuAD knowledge base.

```



\### Step 8 — Medical Entity Recognition



The system identifies basic medical entities from the user's question:



\* Diseases

\* Symptoms

\* Treatments



\### Step 9 — Question Classification



The chatbot detects the type of question:



\* Symptoms

\* Treatment

\* Causes

\* Diagnosis

\* Prevention

\* General Information



\### Step 10 — Display Result



The answer and retrieval information are displayed through the Streamlit interface.



\---



\# 🧬 Medical Entity Recognition



The project implements basic rule/dictionary-based medical entity recognition.



The system currently identifies:



\### Diseases



Examples:



```text

Diabetes

Asthma

Cancer

Hypertension

Leukemia

Pneumonia

Slipped capital femoral epiphysis

```



\### Symptoms



Examples:



```text

Fever

Cough

Headache

Fatigue

Weakness

Shortness of breath

Weight loss

Night sweats

Bleeding

Bruising

Nausea

Vomiting

```



\### Treatments



Examples:



```text

Chemotherapy

Radiation

Surgery

Medication

Immunotherapy

Targeted therapy

Stem cell transplant

```



The entity recognition component is intended as a \*\*basic implementation\*\* for this project.



\---



\# 🔎 Retrieval Mechanism



The retrieval mechanism uses:



```text

TF-IDF + Cosine Similarity

```



\## TF-IDF



TF-IDF converts text into numerical representations based on the importance of words in the questions.



\## Cosine Similarity



Cosine Similarity measures how similar the user's question is to the questions stored in the MedQuAD dataset.



The general workflow is:



```text

User Question

&#x20;     ↓

Text Cleaning

&#x20;     ↓

TF-IDF Vector

&#x20;     ↓

Cosine Similarity

&#x20;     ↓

Similarity Scores

&#x20;     ↓

Highest Relevant Match

&#x20;     ↓

MedQuAD Answer

```



\---



\# 🖥️ User Interface



The project uses \*\*Streamlit\*\* to provide a simple web-based interface.



The interface provides:



\* Medical question input

\* Chat history

\* Medical entity information

\* Question type

\* Similarity score

\* Medical focus

\* Retrieved answer

\* Relevance filtering

\* Medical disclaimer

\* Clear chat option

\* Project information sidebar



\---



\# 📂 Project Structure



```text

Medical\_QA\_Chatbot/

│

├── MedQuAD/

│   ├── 1\_CancerGov\_QA/

│   ├── 2\_GARD\_QA/

│   ├── 3\_GHR\_QA/

│   ├── 4\_MPlus\_Health\_Topics\_QA/

│   ├── 5\_NIDDK\_QA/

│   ├── 6\_NINDS\_QA/

│   ├── 7\_SeniorHealth\_QA/

│   ├── 8\_NHLBI\_QA\_XML/

│   ├── 9\_CDC\_QA/

│   ├── 10\_MPlus\_ADAM\_QA/

│   ├── 11\_MPlusDrugs\_QA/

│   └── 12\_MPlusHerbsSupplements\_QA/

│

├── data/

│   └── medquad.csv

│

├── models/

│   ├── tfidf\_matrix.pkl

│   └── tfidf\_vectorizer.pkl

│

├── src/

│   ├── \_\_init\_\_.py

│   ├── chatbot.py

│   ├── entity\_recognition.py

│   ├── qa\_engine.py

│   └── retriever.py

│

├── prepare\_data.py

├── app.py

├── requirements.txt

├── README.md

└── .gitignore

```



\---



\# 🛠️ Technologies Used



| Technology   | Purpose                                  |

| ------------ | ---------------------------------------- |

| Python       | Main programming language                |

| Pandas       | Dataset processing                       |

| Scikit-learn | TF-IDF and Cosine Similarity             |

| Joblib       | Saving/loading trained retrieval objects |

| Streamlit    | Web-based user interface                 |

| spaCy        | NLP environment/basic NLP support        |

| XML Parser   | Processing MedQuAD XML files             |

| MedQuAD      | Medical knowledge base                   |



\---



\# ⚙️ Installation



\## 1. Clone the repository



```bash

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

```



Move into the project:



```bash

cd Medical\_QA\_Chatbot

```



\## 2. Create a virtual environment



Windows:



```bash

python -m venv venv

```



\## 3. Activate the virtual environment



```bash

venv\\Scripts\\activate

```



\## 4. Install dependencies



```bash

pip install -r requirements.txt

```



\## 5. Install the spaCy English model



```bash

python -m spacy download en\_core\_web\_sm

```



\---



\# ▶️ Running the Project



\## Step 1 — Prepare the dataset



Run:



```bash

python prepare\_data.py

```



This processes the MedQuAD XML files and creates:



```text

data/medquad.csv

```



\## Step 2 — Build the retrieval index



Run:



```bash

python src\\retriever.py

```



This creates:



```text

models/tfidf\_vectorizer.pkl

models/tfidf\_matrix.pkl

```



\## Step 3 — Run the Streamlit application



Run:



```bash

streamlit run app.py

```



The application will be available locally through the Streamlit URL displayed in the terminal.



\---



\# 🧪 Testing



The chatbot was tested using medical and non-medical questions.



\## Test Case 1 — Exact Medical Question



\*\*Question:\*\*



```text

What are the symptoms of Slipped capital femoral epiphysis?

```



\*\*Result:\*\*



```text

Similarity: 100%

```



The correct MedQuAD question and answer were retrieved.



\---



\## Test Case 2 — Reworded Medical Question



\*\*Question:\*\*



```text

What signs can occur with slipped capital femoral epiphysis?

```



\*\*Result:\*\*



```text

Similarity: 87.17%

```



The system successfully retrieved the relevant medical question despite the different wording.



\---



\## Test Case 3 — Non-Medical Question



\*\*Question:\*\*



```text

What is the capital of India?

```



\*\*Similarity:\*\*



```text

35%

```



Since the score was below the 50% threshold, the chatbot correctly rejected the result and displayed:



```text

I could not find a sufficiently relevant medical

answer in the MedQuAD knowledge base.

```



This prevents unrelated questions from receiving irrelevant medical answers.



\---



\# 📊 Example Interaction



\### User



```text

What are the symptoms of Slipped capital femoral epiphysis?

```



\### Medical Entity



```text

Disease:

Slipped capital femoral epiphysis

```



\### Question Type



```text

Symptoms

```



\### Similarity



```text

100%

```



\### Retrieved Medical Focus



```text

Slipped capital femoral epiphysis

```



\### Answer



The chatbot retrieves the corresponding answer from the MedQuAD knowledge base.



\---



\# ⚠️ Limitations



The current version has several limitations:



1\. Medical entity recognition is dictionary/rule based.

2\. The system does not provide medical diagnosis.

3\. The chatbot does not generate new medical knowledge.

4\. Retrieval quality depends on the wording of the user's question.

5\. TF-IDF is mainly lexical and may not fully understand semantic meaning.

6\. The medical entity dictionary covers only a limited set of terms.

7\. The system should not be used as a replacement for a healthcare professional.

8\. The current system does not independently verify the medical information retrieved from the dataset.



\---



\# 🔮 Future Scope



The project can be improved in the future by implementing:



\### 1. Semantic Search



Use sentence-transformer embeddings instead of only TF-IDF.



\### 2. Vector Database



Use systems such as FAISS or another vector database for efficient retrieval from larger medical datasets.



\### 3. Advanced Medical NER



Use a medical-domain NLP model to recognize a wider range of:



\* Diseases

\* Symptoms

\* Drugs

\* Procedures

\* Body parts

\* Medical conditions



\### 4. Better Question Understanding



Implement transformer-based models to understand questions with different wording.



\### 5. Multilingual Support



Support questions in multiple languages.



\### 6. Voice Interaction



Add speech-to-text and text-to-speech capabilities.



\### 7. Improved Conversation Context



Use previous questions to understand follow-up questions.



\### 8. Source Display



Display the source of the retrieved medical information to improve transparency.



\---



\# 🔐 Medical Safety Disclaimer



This chatbot is developed for \*\*educational and demonstration purposes only\*\*.



It should not be used to:



\* Diagnose a medical condition

\* Recommend personal treatment

\* Replace a doctor or healthcare professional

\* Make emergency medical decisions



Users should consult a qualified healthcare professional for medical diagnosis and treatment.



\---



\# 📌 Conclusion



The Medical Q\&A Chatbot demonstrates how a retrieval-based Natural Language Processing system can be developed using the MedQuAD dataset.



The system processes medical XML data, converts questions into TF-IDF vectors, calculates Cosine Similarity, retrieves relevant medical answers, identifies basic medical entities, classifies question types, and presents the results through an interactive Streamlit interface.



The relevance threshold also helps prevent the chatbot from returning unrelated medical answers to non-medical questions.



The project provides a practical implementation of \*\*Natural Language Processing, Information Retrieval, Medical Question Answering, and Streamlit application development\*\*.



\---



\# 👩‍💻 Author



\*\*Sujata Mali\*\*



Medical Q\&A Chatbot Project



\---



\# 📄 License and Dataset Attribution



This project uses the MedQuAD dataset.



Please refer to the original MedQuAD repository and its included license for the dataset's terms of use:



https://github.com/abachaa/MedQuAD



The project code and the dataset should be treated separately with respect to their respective licensing and usage terms.



