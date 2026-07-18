import faiss
import numpy as np

class ResumeSearch:

    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)

    def add(self, embeddings):
        self.index.add(np.array(embeddings))

    def search(self, query_embedding, k):
        distances, indices = self.index.search(
            np.array(query_embedding),
            k
        )

        return distances, indices