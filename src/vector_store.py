# src/store.py
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer

# 1. Initialize your specific embedding model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def get_embedding(text: str):
    """Generates embedding vector for a single text chunk."""
    return model.encode(text).tolist()

def get_embeddings_bulk(texts: list[str]):
    """Generates embeddings efficiently for multiple text chunks."""
    return model.encode(texts).tolist()

def save_chunks_to_db(chunks: list[dict], db_path: str = "../chroma_db"):
    """
    Takes structural chunk dictionaries and saves their raw text, 
    calculated vectors, and tracking metadata directly into a local ChromaDB.
    """
    if not chunks:
        print("⚠️ No chunks provided to save.")
        return

    # Initialize a persistent local database client on your hard drive
    client = chromadb.PersistentClient(path=db_path)
    
    # Create or get an existing collection
    collection = client.get_or_create_collection(name="resume_chunks")

    print(f"Baking embeddings for {len(chunks)} fragments...")
    
    # Unpack document list values for batch processing
    texts = [chunk["content"] for chunk in chunks]
    embeddings = get_embeddings_bulk(texts)
    
    # Build distinct IDs and unpack metadata objects
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [{
        "filename": chunk["file_name"],
        "career": chunk["career_field"]
    } for chunk in chunks]

    # Save everything into the local database
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=texts
    )
    
    print(f"✅ Successfully index and stored {len(chunks)} chunks in local database!")

if __name__ == "__main__":
    # Expects chunks structure matching your raw dict outputs:
    # chunks = [{"file_name": "...", "career_field": "...", "content": "..."}]
    
    # Terminal install: pip install chromadb
    pass
