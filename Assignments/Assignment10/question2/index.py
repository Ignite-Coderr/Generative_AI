import faiss
import numpy as np
from typing import List, Tuple


# Embedding function (dummy for demo)
def embed_text(text: str) -> np.ndarray:
    """
    Converts input text into an embedding vector.
    Replace this with a real embedding model.
    """
    np.random.seed(abs(hash(text)) % (10**8))   # deterministic for demo
    return np.random.rand(1536).astype(np.float32)


# Similarity Search Function
def faiss_similarity_search(
        query: str,
        index: faiss.Index,
        documents: List[str],
        top_k: int = 5
) -> List[Tuple[str, float]]:
    """
    Perform similarity search on a FAISS index.

    Args:
        query (str): User input query
        index (faiss.Index): Pre-built FAISS index
        documents (List[str]): Original text chunks
        top_k (int): Number of similar results to return

    Returns:
        List of tuples -> (text_chunk, similarity_score)
    """

    # 1️⃣ Convert query text into embedding
    query_embedding = embed_text(query)

    # 2️⃣ Reshape for FAISS (expects 2D array)
    query_embedding = query_embedding.reshape(1, -1)

    # 3️⃣ Perform similarity search
    distances, indices = index.search(query_embedding, top_k)

    # 4️⃣ Collect results
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if idx != -1:
            results.append((documents[idx], float(dist)))

    return results


# ------------------ DEMO ------------------

# Sample documents
documents = [
    "Machine learning is a subset of AI.",
    "Deep learning uses neural networks.",
    "FAISS is used for similarity search.",
    "MongoDB stores documents.",
    "Vector databases enable semantic search."
]

# Create embeddings
embeddings = np.array([embed_text(doc) for doc in documents])

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Query
query = "How does semantic search work?"

results = faiss_similarity_search(
    query=query,
    index=index,
    documents=documents,
    top_k=3
)

for text, score in results:
    print(f"Distance: {score:.4f} | Text: {text}")
