from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid
from typing import List, Dict, Any

from .config import Config

class QuadrantStore:
    def __init__(self):
        # Initialize client with provided host/port or in-memory if not available (for simplified local testing without docker)
        # But per requirements docker is used, so we expect a running instance usually.
        # However, for robustness, if connection fails, we might want to warn.
        try:
           self.client = QdrantClient(host=Config.QD_HOST, port=Config.QD_PORT)
           # Test connection
           self.client.get_collections()
        except:
           print("Warning: Could not connect to Qdrant server. Using in-memory storage for fallback/testing.")
           self.client = QdrantClient(":memory:")

    def create_collection(self, collection_name: str, vector_size: int = 1536):
        """Creates a collection if it doesn't exist."""
        try:
            self.client.get_collection(collection_name=collection_name)
            # print(f"Collection {collection_name} already exists.")
        except Exception:
            print(f"Creating collection: {collection_name}")
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size, 
                    distance=models.Distance.COSINE
                )
            )

    def upsert_chunks(self, collection_name: str, chunks: List[str], metadatas: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Upserts chunks with metadata and embeddings into a collection."""
        points = []
        for i, chunk in enumerate(chunks):
            # Generate a UUID based on content or random
            point_id = str(uuid.uuid4())
            points.append(models.PointStruct(
                id=point_id,
                vector=embeddings[i],
                payload={
                    "text": chunk,
                    **metadatas[i]
                }
            ))
            
        self.client.upsert(
            collection_name=collection_name,
            points=points
        )
        print(f"Upserted {len(points)} points to {collection_name}")

    def search(self, collection_name: str, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Searches for similar chunks in a specific collection."""
        try:
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit
            )
            return results
        except Exception as e:
            print(f"Search failed: {e}")
            return []
