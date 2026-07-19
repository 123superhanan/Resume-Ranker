import os
import sys
import streamlit as st

# Add src folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Import your existing code
from src.parser import extract_text
from src.chunker import chunk_text
from src.embedder import create_embeddings, embed_query
from src.prompt_maker import ResumeSearch  

st.set_page_config(
    page_title="AI Resume Ranker",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Load Data Once
# -----------------------------
@st.cache_resource
def build_search_engine():

    resume_folder = os.path.join(os.path.dirname(__file__), "data")

    documents = []

    count = 0
    MAX_RESUMES = 30

    for root, dirs, files in os.walk(resume_folder):

        for file in files:

            if count >= MAX_RESUMES:
                break

            if not file.lower().endswith(".pdf"):
                continue

            path = os.path.join(root, file)

            text = extract_text(path)

            chunks = chunk_text(text)

            for chunk in chunks:

                documents.append({
                    "resume": file,
                    "category": os.path.basename(root),
                    "text": chunk
                })

            count += 1

        if count >= MAX_RESUMES:
            break

    texts = [doc["text"] for doc in documents]

    embeddings = create_embeddings(texts)

    search_engine = ResumeSearch(embeddings.shape[1])

    search_engine.add(embeddings)

    return search_engine, documents


search_engine, documents = build_search_engine()

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("Resume Ranker")

    st.info(f"Loaded Resumes: 30")

    st.info(f"Indexed Chunks: {len(documents)}")

    top_k = st.slider(
        "Top Results",
        1,
        10,
        5
    )

# -----------------------------
# Main UI
# -----------------------------
st.title("📄 AI Resume Ranker")

st.write(
    "Paste a Job Description below and rank resumes using semantic search."
)

job_description = st.text_area(
    "Job Description",
    height=250,
    placeholder="Example:\n\nLooking for a Backend Engineer with Python, FastAPI, Docker and PostgreSQL..."
)

search = st.button("🔍 Rank Resumes", use_container_width=True)

if search:

    if job_description.strip() == "":
        st.warning("Please enter a Job Description.")
        st.stop()

    with st.spinner("Searching resumes..."):

        query_embedding = embed_query(job_description)

        distances, indices = search_engine.index.search(
            query_embedding,
            top_k
        )

    st.success("Search Complete")

    st.divider()

    st.subheader("Top Matches")

    for rank, (score, idx) in enumerate(zip(distances[0], indices[0]), start=1):

        doc = documents[idx]

        with st.container(border=True):

            col1, col2 = st.columns([5, 1])

            with col1:

                st.markdown(f"### 🏆 Rank #{rank}")

                st.write(f"**Resume:** {doc['resume']}")

                st.write(f"**Category:** {doc['category']}")

                st.write(doc["text"][:400] + "...")

            with col2:

                similarity = max(0, 100 - score)

                st.metric(
                    "Score",
                    f"{similarity:.1f}%"
                )