import os
import numpy as np
from parser import extract_text
from chunker import chunk_text
from embedder import create_embeddings
from embedder import embed_query
from prompt_maker import ResumeSearch


BASE_DIR = os.path.dirname(__file__)

resume_folder = os.path.join(BASE_DIR, "..", "data") 
documents = []
count = 0
MAX_RESUMES = 30

for root, dirs, files in os.walk(resume_folder):

    for file in files:

        if not file.lower().endswith(".pdf"):
            continue

        if count >= MAX_RESUMES:
            break

        path = os.path.join(root, file)

        print(f"Loading: {file}")

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

print(f"Loaded {count} resumes")
print(f"Created {len(documents)} chunks")

texts = [doc["text"] for doc in documents]

embeddings = create_embeddings(texts)
embeddings_array = np.array(embeddings)
dimension = embeddings_array.shape[-1]

search_engine = ResumeSearch(dimension)

search_engine.add(embeddings_array)

job_description = input("\nEnter Job Description:\n")

query_embedding = embed_query(job_description)

results = search_engine.search(query_embedding, k=5)

print("\nTop Matches\n")

for idx in results:

    print("=" * 50)

    print("Resume :", documents[idx]["resume"])

    print()

    print(documents[idx]["text"][:300])