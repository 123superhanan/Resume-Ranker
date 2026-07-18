from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def create_embeddings(texts):
    return model.encode(texts)

def embed_query(query):
    return model.encode([query])