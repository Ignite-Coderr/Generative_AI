import numpy as np
from .openai_client import OpenAIClient
from .config import Config

class SectionRouter:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
        self.section_embeddings = {}
        # Compute embeddings for section descriptions on startup
        self._initialize_embeddings()

    def _initialize_embeddings(self):
        """Generates embeddings for all section descriptions."""
        print("Initializing Section Router...")
        for section, description in Config.SECTION_DESCRIPTIONS.items():
            self.section_embeddings[section] = self.openai_client.get_embedding(description)
        print("Section Router Initialized.")

    def route_query(self, query):
        """
        Determines the most appropriate section for the given query.
        Returns: (selected_section, similarity_score, explanation)
        """
        query_embedding = self.openai_client.get_embedding(query)
        if query_embedding is None:
            return None, 0.0, "Error generating embedding."

        best_section = None
        max_similarity = -1.0
        
        # Calculate cosine similarity with each section
        similarities = {}
        
        for section, embedding in self.section_embeddings.items():
            similarity = np.dot(query_embedding, embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(embedding))
            similarities[section] = similarity
            
            if similarity > max_similarity:
                max_similarity = similarity
                best_section = section
                
        explanation = self._generate_explanation(query, best_section, max_similarity)
        
        return best_section, max_similarity, explanation, similarities

    def _generate_explanation(self, query, section, score):
        """Generates a simple explanation based on the selection."""
        base_explanation = f"Query was most similar to the '{section}' section with a score of {score:.4f}."
        
        if score < 0.3:
            return base_explanation + " Note: The similarity is quite low, so the relevance might be minimal."
            
        return base_explanation
