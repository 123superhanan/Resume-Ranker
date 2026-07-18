
# Resume Ranker
A Retrieval-Augmented Generation (RAG) system that ranks and evaluates resumes against a job description, using local embeddings, a vector database, and a local LLM for reasoning — with a Streamlit interface for interaction.
---## Table of Contents- [Overview](#overview)
- [What is RAG?](#what-is-rag)
- [Why RAG for Resume Ranking?](#why-rag-for-resume-ranking)
- [System Architecture](#system-architecture)
- [Pipeline Breakdown](#pipeline-breakdown)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Design Decisions](#design-decisions)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Learnings](#learnings)
---## Overview
Resume Ranker takes a set of resumes (PDF) and a job description, then uses semantic search plus an LLM to score and explain how well each resume matches the role. Instead of relying on keyword matching, it retrieves the most *semantically relevant* sections of each resume and asks an LLM to reason over them.

This is a learning-oriented implementation — the goal is to understand every stage of a RAG pipeline (chunking, embedding, retrieval, prompt construction, generation) by building it from scratch rather than relying on a framework like LangChain.
---## What is RAG?
**Retrieval-Augmented Generation (RAG)** is a technique that grounds an LLM's response in external data instead of relying purely on what the model memorized during training.

Standard flow:

Query → LLM → Answer (based only on training data)


RAG flow:

Query → Retrieve relevant context from a knowledge base → Inject context into prompt → LLM → Answer (grounded in real data)


This matters here because a general-purpose LLM has no idea what's inside *your* resumes or *your* job description — RAG is what lets it reason about your specific documents instead of hallucinating.

---

## Why RAG for Resume Ranking?

- Resumes and job descriptions are unstructured text — a good fit for semantic (meaning-based) search rather than exact keyword matching
- A candidate might describe a skill differently than the job description phrases it (e.g. "built REST APIs" vs "backend development experience") — embeddings capture that similarity, keyword search doesn't
- The LLM only needs to reason over the *relevant* chunks of a resume, not the entire document, which keeps prompts smaller and answers more focused

---

## System Architecture


┌─────────────┐
│ PDF Resumes │
└──────┬──────┘
│
Text Extraction
│
▼
┌───────────┐
│ Chunking │
└─────┬─────┘
│
▼
┌───────────┐
│ Embedding │ (Ollama embedding model)
└─────┬─────┘
│
▼
┌─────────────────┐
│ Vector Store │ (ChromaDB)
└────────┬─────────┘
│
Job Description (query) ──► Embed ──► Retrieve top-N chunks
│
▼
┌───────────────────┐
│ Prompt Construction │
└──────────┬────────┘
│
▼
┌─────────────┐
│ LLM (Ollama) │
└──────┬──────┘
│
▼
┌─────────────────┐
│ Ranking + Reason │
└─────────┬────────┘
│
▼
┌───────────────┐
│ Streamlit UI │
└───────────────┘


---

## Pipeline Breakdown

- **Loader** (`src/loader.py`): Extracts raw text from uploaded PDF resumes and Job Descriptions.
- **Chunker** (`src/chunker.py`): Splits text into overlapping semantic chunks to maintain context.
- **Embedder** (`src/embedder.py`): Generates vector embeddings using a local sentence-transformers model.
- **Vector Store** (`src/vector_store.py`): Indexes embeddings in an in-memory vector database for fast similarity search.
- **Prompt Maker** (`src/prompt_maker.py`): Formulates a comparative prompt matching candidate chunks against the target JD.
- **Generator** (`src/main.py`): Orchestrates the evaluation workflow and passes structured prompts to a local LLM.
- **UI** (`app.py`): Provides a Streamlit dashboard to upload PDFs, paste JDs, and visualize candidate rankings.

---

## Tech Stack

- **Python** — core pipeline logic
- **pypdf / pdfplumber** — PDF text extraction
- **ChromaDB** — local vector database for storing and querying embeddings
- **Ollama** — runs local embedding model (`nomic-embed-text`) and generation model (`llama3.2` or similar) — no API cost, fully offline
- **Streamlit** — lightweight UI for uploading resumes and viewing results

---

## Project Structure


resume-ranker/
README.md
requirements.txt
data/ # sample resumes + job descriptions for testing
src/
loader.py
chunker.py
embedder.py
vector_store.py
prompt_maker.py
main.py
app.py # Streamlit entry point


---

## Setup & Installation

```bash
git clone https://github.com/<your-username>/resume-ranker.git
cd resume-ranker
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Pull required Ollama models
ollama pull nomic-embed-text
ollama pull llama3.2
```

---

## Usage

```bash
streamlit run app.py
```

1. Upload one or more resumes (PDF)
2. Paste in a job description
3. View ranked resumes with explanations for each score

---

## Design Decisions

- **Chunking with overlap**: prevents important context (e.g. a skill described across two sentences) from being split and losing meaning
- **Local LLM via Ollama**: no API costs during development, full control over prompt/response cycle, and forces understanding of the raw request/response instead of hiding it behind a hosted API
- **ChromaDB over manual vector search**: at this project stage, using a real vector DB is appropriate since retrieval scale (many resumes) benefits from indexed search rather than a manual loop
- **Ranking = many resumes vs one job description**: the job description is used as the *query*, and each resume's most relevant chunks are retrieved and scored against it

---

## Limitations

- Local LLM inference is slower than a hosted API; response time scales with hardware
- No authentication or persistence layer yet — single-session use only
- Ranking quality depends heavily on resume formatting; poorly structured PDFs may extract text out of order

---

## Roadmap

- [ ] Multi-resume batch ranking with sorted output
- [ ] Structured JSON output (score, matched skills, gaps) instead of free text
- [ ] Caching embeddings so re-running doesn't re-embed unchanged resumes
- [ ] Optional cloud LLM fallback for faster responses

---

## Learnings

_(Fill this in as you build — documenting what broke and how you fixed it is genuinely valuable for interviews and shows real engineering process, not just a finished product.)_

