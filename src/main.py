import os
import numpy as np
from parser import extract_text
from chunker import chunk_text
from embedder import create_embeddings, embed_query
from prompt_maker import ResumeSearch

BASE_DIR = os.path.dirname(__file__)
resume_folder = os.path.join(BASE_DIR, "..", "data") 

# 1. Group all PDF paths by their folder first to balance categories
folder_groups = {}
for root, dirs, files in os.walk(resume_folder):
    pdf_files = [f for f in files if f.lower().endswith(".pdf")]
    if pdf_files:
        category_name = os.path.basename(root)
        folder_groups[category_name] = [os.path.join(root, f) for f in pdf_files]

# 2. Pick exactly 3 files from every single category to prevent loading 2000 at once
FILES_PER_CATEGORY = 3 
balanced_file_paths = []

print("--- Category Breakdown ---")
for category, paths in folder_groups.items():
    selected = paths[:FILES_PER_CATEGORY]
    balanced_file_paths.extend(selected)
    print(f"📁 {category}: Selected {len(selected)} out of {len(paths)} resumes.")

print(f"\nTotal selected resumes for pipeline: {len(balanced_file_paths)}\n")

# 3. Process the balanced list
documents = []
for path in balanced_file_paths:
    file_name = os.path.basename(path)
    category_name = os.path.basename(os.path.dirname(path))
    
    print(f"Loading: {category_name}/{file_name}")
    try:
        text = extract_text(path)
        chunks = chunk_text(text)

        for chunk in chunks:
            documents.append({
                "resume": file_name,
                "category": category_name,
                "text": chunk
            })
    except Exception as e:
        print(f"Skipping broken file {file_name}: {e}")

print(f"\nLoaded {len(balanced_file_paths)} resumes")
print(f"Created {len(documents)} total chunks")

# 4. Generate Embeddings
texts = [doc["text"] for doc in documents]
embeddings = create_embeddings(texts)

# Ensure embeddings are forced into a float32 numpy array for FAISS
embeddings_array = np.array(embeddings).astype('float32')
dimension = embeddings_array.shape[-1]

# 5. Build FAISS Index
search_engine = ResumeSearch(dimension)
search_engine.add(embeddings_array)

# 6. Search Query
job_description = input("\nEnter Job Description:\n")
query_embedding = embed_query(job_description)

# Ensure query embedding is a 2D float32 numpy array (shape: [1, dimension])
query_embedding_array = np.array(query_embedding).astype('float32')
if query_embedding_array.ndim == 1:
    query_embedding_array = np.expand_dims(query_embedding_array, axis=0)

# Execute search
distances, indices = search_engine.search(query_embedding_array, k=5)

print("\nTop Matches\n")

# 7. Unpack FAISS 2D outputs using [0] to extract the first query's results
top_indices = indices[0]
top_distances = distances[0]

for rank, idx in enumerate(top_indices):
    # FAISS returns -1 if it can't find enough vectors in a small test set
    if idx == -1:
        continue
        
    print("=" * 50)
    print(f"Rank #{rank + 1} | L2 Distance Score: {top_distances[rank]:.4f}")
    print("Category :", documents[idx]["category"])
    print("Resume   :", documents[idx]["resume"])
    print("-" * 50)
    print(documents[idx]["text"][:300] + "...")
