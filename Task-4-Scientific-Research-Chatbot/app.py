import streamlit as st
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
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Scientific Research Chatbot",
    page_icon="🔬",
    layout="wide"
)


# ============================================================
# LOAD MODELS
# ============================================================

@st.cache_resource
def load_embedding_model():

    return SentenceTransformer(
        EMBEDDING_MODEL
    )


@st.cache_resource
def load_collection():

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    return collection


# ============================================================
# INITIALIZE
# ============================================================

with st.spinner("Loading research database..."):

    embedding_model = load_embedding_model()

    collection = load_collection()


# ============================================================
# SEARCH FUNCTION
# ============================================================

def search_papers(query, number=5):

    embedding = embedding_model.encode(
        [query]
    )[0].tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=number
    )

    return results


# ============================================================
# LLAMA 3 FUNCTION
# ============================================================

def ask_llama(prompt):

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
# PAPER SEARCH DISPLAY
# ============================================================

def display_search_results(results):

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i in range(len(documents)):

        metadata = metadatas[i]

        st.markdown(
            f"### 📄 {i + 1}. {metadata['title']}"
        )

        st.write(
            "**Authors:**",
            metadata["authors"]
        )

        st.write(
            "**Categories:**",
            metadata["categories"]
        )

        st.write(
            "**Similarity Distance:**",
            round(distances[i], 4)
        )

        with st.expander("View Abstract"):

            st.write(
                documents[i]
            )

        st.divider()


# ============================================================
# PAPER SUMMARY
# ============================================================

def summarize_paper(title, abstract):

    prompt = f"""
You are a scientific research assistant.

Summarize the following Computer Science research paper.

TITLE:
{title}

ABSTRACT:
{abstract}

Provide the summary using these sections:

1. Research Problem
2. Main Idea
3. Methodology
4. Important Findings
5. Applications
6. Limitations
7. Simple Explanation

Do not invent information that is not present
in the provided abstract.
"""

    return ask_llama(prompt)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🔬 Research Database")

    st.write(
        f"**Total Papers:** {collection.count():,}"
    )

    st.write(
        "**Domain:** Computer Science"
    )

    st.write(
        "**LLM:** Llama 3"
    )

    st.write(
        "**Vector Database:** ChromaDB"
    )

    st.divider()

    st.info(
        "This chatbot uses arXiv research papers "
        "to answer Computer Science questions."
    )


# ============================================================
# MAIN TITLE
# ============================================================

st.title(
    "🔬 Scientific Research Chatbot"
)

st.write(
    "AI-powered research assistant for Computer Science "
    "research papers using arXiv, ChromaDB and Llama 3."
)


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "💬 Research Assistant",
        "🔎 Paper Search",
        "🧠 Concept Visualization",
        "📄 Paper Summarization",
        "🔍 Information Extraction"
    ]
)
# ============================================================
# TAB 1 — RESEARCH ASSISTANT
# ============================================================

with tab1:

    st.header(
        "💬 Ask the Research Assistant"
    )

    st.write(
        "Ask complex Computer Science research questions."
    )

    if "messages" not in st.session_state:

        st.session_state.messages = []


    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    question = st.chat_input(
        "Ask a scientific research question..."
    )


    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)


        with st.spinner(
            "🔎 Searching research papers..."
        ):

            results = search_papers(
                question,
                TOP_K
            )


        documents = results["documents"][0]
        metadatas = results["metadatas"][0]


        context = ""


        for i in range(len(documents)):

            context += f"""

Paper {i + 1}

Title:
{metadatas[i]["title"]}

Authors:
{metadatas[i]["authors"]}

Categories:
{metadatas[i]["categories"]}

Abstract:
{documents[i]}

"""


        prompt = f"""
You are an expert Computer Science research assistant.

Answer the user's question using the research papers
provided below.

USER QUESTION:
{question}

RESEARCH PAPERS:
{context}

Instructions:

1. Give a clear scientific explanation.
2. Explain difficult concepts simply.
3. Use the research papers as supporting information.
4. Do not invent research findings.
5. Mention relevant papers when useful.
6. If the papers do not contain enough information,
   clearly say so.
"""


        with st.spinner(
            "🤖 Generating answer with Llama 3..."
        ):

            answer = ask_llama(
                prompt
            )


        with st.chat_message(
            "assistant"
        ):

            st.markdown(answer)


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


        st.subheader(
            "📚 Research Sources"
        )

        display_search_results(
            results
        )


# ============================================================
# TAB 2 — PAPER SEARCH
# ============================================================

with tab2:

    st.header(
        "🔎 Search Scientific Papers"
    )

    st.write(
        "Search the 9,932 Computer Science papers "
        "using semantic search."
    )


    search_query = st.text_input(
        "Enter a research topic",
        placeholder="Example: Transformer architecture in NLP"
    )


    number_of_results = st.slider(
        "Number of papers",
        min_value=1,
        max_value=10,
        value=5
    )


    search_button = st.button(
        "🔎 Search Papers"
    )


    if search_button:

        if search_query.strip() == "":

            st.warning(
                "Please enter a research topic."
            )

        else:

            with st.spinner(
                "Searching scientific papers..."
            ):

                results = search_papers(
                    search_query,
                    number_of_results
                )


            st.success(
                f"Found {number_of_results} relevant papers."
            )


            display_search_results(
                results
            )


# ============================================================
# TAB 3 — CONCEPT VISUALIZATION
# ============================================================

with tab3:

    st.header(
        "🧠 Concept Visualization"
    )

    st.write(
        "Enter a Computer Science concept to generate "
        "a simple conceptual explanation."
    )


    concept = st.text_input(
        "Enter concept",
        placeholder="Example: Transformer"
    )


    visualize_button = st.button(
        "🧠 Explain Concept"
    )


    if visualize_button:

        if concept.strip() == "":

            st.warning(
                "Please enter a concept."
            )

        else:

            with st.spinner(
                "Analyzing concept..."
            ):

                results = search_papers(
                    concept,
                    5
                )


                documents = results["documents"][0]
                metadatas = results["metadatas"][0]


                context = ""


                for i in range(len(documents)):

                    context += f"""

Title:
{metadatas[i]["title"]}

Abstract:
{documents[i]}

"""


                prompt = f"""
You are a Computer Science teacher.

Explain the concept:

{concept}

Use the following research papers:

{context}

Create a simple explanation with:

1. Definition
2. Main Components
3. How It Works
4. Applications
5. Advantages
6. Limitations
7. Simple Example

Keep the explanation suitable for a student.
"""


                explanation = ask_llama(
                    prompt
                )


            st.markdown(
                explanation
            )
# ============================================================
# TAB 4 — PAPER SUMMARIZATION
# ============================================================

with tab4:

    st.header("📄 Research Paper Summarization")

    st.write(
        "Search for a research paper and generate an AI-powered "
        "summary using Llama 3."
    )

    summary_query = st.text_input(
        "Enter paper title or research topic",
        placeholder="Example: Transformer architecture"
    )

    summary_search_button = st.button(
        "🔎 Find Paper"
    )

    if summary_search_button:

        if summary_query.strip() == "":

            st.warning(
                "Please enter a paper title or research topic."
            )

        else:

            with st.spinner(
                "Searching research papers..."
            ):

                summary_results = search_papers(
                    summary_query,
                    5
                )

            documents = summary_results["documents"][0]
            metadatas = summary_results["metadatas"][0]

            st.session_state["summary_documents"] = documents
            st.session_state["summary_metadatas"] = metadatas

    # --------------------------------------------------------
    # SHOW SEARCH RESULTS
    # --------------------------------------------------------

    if "summary_metadatas" in st.session_state:

        metadatas = st.session_state["summary_metadatas"]
        documents = st.session_state["summary_documents"]

        paper_titles = [
            metadata["title"]
            for metadata in metadatas
        ]

        selected_paper = st.selectbox(
            "Select a research paper",
            paper_titles
        )

        selected_index = paper_titles.index(
            selected_paper
        )

        selected_metadata = metadatas[selected_index]
        selected_abstract = documents[selected_index]

        st.subheader("📄 Selected Paper")

        st.write(
            "**Title:**",
            selected_metadata["title"]
        )

        st.write(
            "**Authors:**",
            selected_metadata["authors"]
        )

        st.write(
            "**Categories:**",
            selected_metadata["categories"]
        )

        with st.expander("📖 View Original Abstract"):

            st.write(
                selected_abstract
            )

        summarize_button = st.button(
            "🤖 Generate Summary with Llama 3"
        )

        if summarize_button:

            prompt = f"""
You are an expert Computer Science research assistant.

Analyze the following research paper abstract.

PAPER TITLE:
{selected_metadata["title"]}

AUTHORS:
{selected_metadata["authors"]}

ABSTRACT:
{selected_abstract}

Create a structured research summary.

Use exactly these sections:

## 1. Research Problem
Explain what problem the paper tries to solve.

## 2. Main Idea
Explain the central idea of the research.

## 3. Methodology
Explain the approach or method used.

## 4. Key Findings
Explain the important results or conclusions.

## 5. Applications
Explain where this research can be useful.

## 6. Limitations
Mention limitations if they are stated or can be
clearly identified from the abstract.

## 7. Simple Explanation
Explain the paper in simple language suitable for
a Computer Science student.

IMPORTANT:
Use only information available in the provided abstract.
Do not invent results, experiments, datasets, or claims.
"""

            with st.spinner(
                "🤖 Llama 3 is generating the summary..."
            ):

                summary = ask_llama(
                    prompt
                )

            st.subheader(
                "📋 AI-Generated Research Summary"
            )

            st.markdown(
                summary
            )

            st.success(
                "Paper summary generated successfully."
            )
   # ============================================================
# TAB 5 — INFORMATION EXTRACTION
# ============================================================

with tab5:

    st.header("🔍 Research Information Extraction")

    st.write(
        "Extract important research information from "
        "scientific papers using Llama 3."
    )

    extraction_query = st.text_input(
        "Enter a paper title or research topic",
        placeholder="Example: Machine Learning"
    )

    extraction_search_button = st.button(
        "🔎 Find Research Paper",
        key="extraction_search"
    )

    if extraction_search_button:

        if extraction_query.strip() == "":

            st.warning(
                "Please enter a paper title or research topic."
            )

        else:

            with st.spinner(
                "Searching research papers..."
            ):

                extraction_results = search_papers(
                    extraction_query,
                    5
                )

            st.session_state[
                "extraction_documents"
            ] = extraction_results["documents"][0]

            st.session_state[
                "extraction_metadatas"
            ] = extraction_results["metadatas"][0]


    # --------------------------------------------------------
    # DISPLAY PAPERS
    # --------------------------------------------------------

    if "extraction_metadatas" in st.session_state:

        metadatas = st.session_state[
            "extraction_metadatas"
        ]

        documents = st.session_state[
            "extraction_documents"
        ]

        paper_titles = [
            metadata["title"]
            for metadata in metadatas
        ]

        selected_paper = st.selectbox(
            "Select a research paper",
            paper_titles,
            key="extraction_paper"
        )

        selected_index = paper_titles.index(
            selected_paper
        )

        selected_metadata = metadatas[
            selected_index
        ]

        selected_abstract = documents[
            selected_index
        ]

        st.subheader("📄 Selected Paper")

        st.write(
            "**Title:**",
            selected_metadata["title"]
        )

        st.write(
            "**Authors:**",
            selected_metadata["authors"]
        )

        st.write(
            "**Categories:**",
            selected_metadata["categories"]
        )

        with st.expander("📖 View Abstract"):

            st.write(
                selected_abstract
            )

        extract_button = st.button(
            "🔍 Extract Research Information",
            key="extract_information"
        )

        if extract_button:

            prompt = f"""
You are an expert Computer Science research assistant.

Extract structured information from the following
research paper.

TITLE:
{selected_metadata["title"]}

AUTHORS:
{selected_metadata["authors"]}

CATEGORIES:
{selected_metadata["categories"]}

ABSTRACT:
{selected_abstract}

Extract the following information:

1. Research Problem
2. Research Objective
3. Methodology
4. Key Technologies or Techniques
5. Dataset or Data Used
6. Key Findings
7. Applications
8. Limitations
9. Important Keywords

Rules:

- Use only information available in the paper abstract.
- Do not invent information.
- If information is not available, write:
  "Not specified in the abstract."
- Keep each answer concise.
- Return the information using clear headings.
"""

            with st.spinner(
                "🤖 Extracting research information with Llama 3..."
            ):

                extracted_information = ask_llama(
                    prompt
                )

            st.subheader(
                "📊 Extracted Research Information"
            )

            st.markdown(
                extracted_information
            )

            st.success(
                "Research information extracted successfully."
            )
# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Scientific Research Chatbot | "
    "arXiv + ChromaDB + Sentence Transformers + Llama 3"
)