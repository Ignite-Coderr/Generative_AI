"""
Embedding Store Module

This module handles the creation and storage of embeddings using FAISS vector database.
It converts model descriptions into embeddings and enables similarity-based search.
"""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import os


class EmbeddingStore:
    """
    Vector store for model embeddings using FAISS
    
    This class handles:
    - Embedding generation using sentence-transformers
    - Vector storage and indexing with FAISS
    - Similarity search for query routing
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding store
        
        Args:
            model_name: Name of the sentence-transformer model to use
        """
        print(f"Loading embedding model: {model_name}...")
        self.embedding_model = SentenceTransformer(model_name)
        self.index = None
        self.dimension = None
        self.model_names = []
        print("Embedding model loaded successfully!")
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            Numpy array of embeddings
        """
        print(f"Creating embeddings for {len(texts)} texts...")
        embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
        print(f"Embeddings created with shape: {embeddings.shape}")
        return embeddings
    
    def build_index(self, model_descriptions: List[str], model_names: List[str]):
        """
        Build FAISS index from model descriptions
        
        Args:
            model_descriptions: List of model description texts
            model_names: Corresponding list of model names
        """
        print("\n" + "="*60)
        print("Building FAISS Vector Index")
        print("="*60)
        
        # Store model names for later retrieval
        self.model_names = model_names
        
        # Generate embeddings
        embeddings = self.create_embeddings(model_descriptions)
        self.dimension = embeddings.shape[1]
        
        # Create FAISS index (L2 distance)
        print(f"Creating FAISS index with dimension: {self.dimension}")
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Add embeddings to index
        self.index.add(embeddings.astype('float32'))
        print(f"Added {self.index.ntotal} vectors to index")
        print("="*60 + "\n")
    
    def search(self, query: str, k: int = 1) -> List[Tuple[str, float]]:
        """
        Search for the most similar model based on query
        
        Args:
            query: User query string
            k: Number of top results to return
            
        Returns:
            List of tuples (model_name, similarity_score)
        """
        if self.index is None:
            raise ValueError("Index not built. Call build_index() first.")
        
        # Generate query embedding
        query_embedding = self.create_embeddings([query])
        
        # Search in FAISS index
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Convert L2 distances to similarity scores (0-1 range)
        # Lower distance = higher similarity
        # We use inverse exponential to convert distance to similarity
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            similarity = np.exp(-dist / 10)  # Normalize distance to similarity
            model_name = self.model_names[idx]
            results.append((model_name, float(similarity)))
        
        return results
    
    def save_index(self, path: str):
        """
        Save FAISS index to disk
        
        Args:
            path: Directory path to save the index
        """
        if self.index is None:
            raise ValueError("No index to save. Build index first.")
        
        os.makedirs(path, exist_ok=True)
        index_path = os.path.join(path, "faiss_index.bin")
        faiss.write_index(self.index, index_path)
        
        # Save model names
        names_path = os.path.join(path, "model_names.txt")
        with open(names_path, 'w') as f:
            f.write('\n'.join(self.model_names))
        
        print(f"Index saved to {path}")
    
    def load_index(self, path: str):
        """
        Load FAISS index from disk
        
        Args:
            path: Directory path containing the saved index
        """
        index_path = os.path.join(path, "faiss_index.bin")
        self.index = faiss.read_index(index_path)
        
        # Load model names
        names_path = os.path.join(path, "model_names.txt")
        with open(names_path, 'r') as f:
            self.model_names = f.read().strip().split('\n')
        
        print(f"Index loaded from {path}")
