import os

from parser import extract_text
from chunker import chunk_text
from embedder import create_embeddings
from embedder import embed_query
from prompt_maker import ResumeSearch

documents = []

resume_folder = "resumes"

for file in os.listdir(resume_folder):

    if not file.endswith(".pdf"):
        continue

    path = os.path.join(resume_folder, file)

    print(f"Loading {file}")

    text = extract_text(path)

    chunks = chunk_text(text)

    for chunk in chunks:

        documents.append(
            {
                "resume": file,
                "text": chunk
            }
        )

print(f"\nLoaded {len(documents)} chunks")

texts = [doc["text"] for doc in documents]

embeddings = create_embeddings(texts)

dimension = embeddings.shape[1]

search_engine = ResumeSearch(dimension)

search_engine.add(embeddings)

job_description = input("\nEnter Job Description:\n")

query_embedding = embed_query(job_description)

results = search_engine.search(query_embedding, k=5)

print("\nTop Matches\n")

for idx in results:

    print("=" * 50)

    print("Resume :", documents[idx]["resume"])

    print()

    print(documents[idx]["text"][:300])