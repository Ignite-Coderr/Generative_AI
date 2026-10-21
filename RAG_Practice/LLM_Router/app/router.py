"""
Router Module

This module implements the intelligent routing logic that:
1. Analyzes user queries
2. Determines complexity and intent
3. Selects the most appropriate model
4. Generates routing explanations
"""

from typing import Dict, Any
from .model_registry import ModelRegistry
from .embedding_store import EmbeddingStore
from .utils import analyze_query_complexity, determine_intent


class IntelligentRouter:
    """
    Main routing engine for selecting optimal AI models
    
    This class orchestrates the routing process by:
    - Analyzing query characteristics
    - Performing embedding-based similarity search
    - Generating detailed routing explanations
    """
    
    def __init__(self):
        """Initialize the router with model registry and embedding store"""
        print("\n" + "="*60)
        print("Initializing Intelligent Model Router")
        print("="*60)
        
        # Initialize components
        self.registry = ModelRegistry()
        self.embedding_store = EmbeddingStore()
        
        # Build embedding index
        self._build_index()
        
        print("Router initialization complete!")
        print("="*60 + "\n")
    
    def _build_index(self):
        """Build the FAISS index with model descriptions"""
        model_descriptions = self.registry.get_model_descriptions()
        model_names = self.registry.get_model_names()
        self.embedding_store.build_index(model_descriptions, model_names)
    
    def route(self, query: str) -> Dict[str, Any]:
        """
        Route a user query to the most appropriate model
        
        Args:
            query: User's input query
            
        Returns:
            Dictionary containing:
                - selected_model: Name of chosen model
                - model_info: Full model information
                - similarity_score: Embedding similarity score
                - routing_analysis: Detailed analysis of routing decision
        """
        print(f"\n{'='*60}")
        print(f"Routing Query: {query}")
        print(f"{'='*60}")
        
        # Step 1: Analyze query characteristics
        print("\n[1/3] Analyzing query characteristics...")
        intent = determine_intent(query)
        complexity = analyze_query_complexity(query)
        
        print(f"  ├─ Intent: {intent}")
        print(f"  └─ Complexity: {complexity}")
        
        # Step 2: Perform embedding-based search
        print("\n[2/3] Performing embedding-based similarity search...")
        results = self.embedding_store.search(query, k=1)
        selected_model_name, similarity_score = results[0]
        
        print(f"  ├─ Best Match: {selected_model_name}")
        print(f"  └─ Similarity Score: {similarity_score:.4f}")
        
        # Step 3: Get full model information
        print("\n[3/3] Retrieving model information...")
        model_info = self.registry.get_model_by_name(selected_model_name)
        
        # Generate routing explanation
        routing_analysis = self._generate_routing_explanation(
            query, intent, complexity, selected_model_name, similarity_score, model_info
        )
        
        print(f"\n{'='*60}")
        print(f"Routing Complete: {selected_model_name}")
        print(f"{'='*60}\n")
        
        return {
            "selected_model": selected_model_name,
            "model_info": model_info,
            "similarity_score": similarity_score,
            "routing_analysis": routing_analysis
        }
    
    def _generate_routing_explanation(
        self, 
        query: str,
        intent: str,
        complexity: str,
        model_name: str,
        similarity: float,
        model_info: Any
    ) -> Dict[str, Any]:
        """
        Generate a detailed explanation of the routing decision
        
        Args:
            query: Original user query
            intent: Detected query intent
            complexity: Detected complexity level
            model_name: Selected model name
            similarity: Similarity score
            model_info: Full model information object
            
        Returns:
            Dictionary with routing analysis details
        """
        # Generate human-readable explanation
        explanation = self._create_explanation_text(
            intent, complexity, model_name, similarity
        )
        
        return {
            "query": query,
            "detected_intent": intent,
            "complexity_level": complexity,
            "selected_model": model_name,
            "similarity_score": round(similarity, 4),
            "model_complexity": model_info.complexity.value,
            "model_cost": model_info.cost.value,
            "model_latency": model_info.latency.value,
            "explanation": explanation
        }
    
    def _create_explanation_text(
        self, 
        intent: str, 
        complexity: str, 
        model_name: str, 
        similarity: float
    ) -> str:
        """
        Create human-readable explanation text
        
        Args:
            intent: Query intent
            complexity: Complexity level
            model_name: Selected model
            similarity: Similarity score
            
        Returns:
            Formatted explanation string
        """
        reasons = []
        
        # Intent-based reasoning
        if intent == "arithmetic":
            reasons.append("the query involves basic arithmetic operations")
        elif intent == "mathematical":
            reasons.append("the query requires advanced mathematical reasoning")
        elif intent == "explanatory":
            reasons.append("the query asks for detailed explanation or research-level content")
        elif intent == "creative":
            reasons.append("the query is creative, humorous, or entertainment-focused")
        
        # Complexity-based reasoning
        if complexity == "low":
            reasons.append("it has low computational complexity")
        elif complexity == "medium":
            reasons.append("it involves multi-step reasoning")
        elif complexity == "high":
            reasons.append("it requires deep analysis and comprehensive response")
        
        # Similarity-based reasoning
        confidence = "high" if similarity > 0.7 else "moderate" if similarity > 0.5 else "low"
        reasons.append(f"embedding similarity indicates {confidence} confidence match")
        
        explanation = (
            f"Selected **{model_name}** because {', '.join(reasons)}. "
            f"This model is optimized for this type of query."
        )
        
        return explanation
