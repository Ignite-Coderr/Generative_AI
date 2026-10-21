from .section_router import SectionRouter
from .quadrant_store import QuadrantStore
from .openai_client import OpenAIClient
from .config import Config

class RAGPipeline:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.router = SectionRouter(self.openai_client)
        self.quadrant_store = QuadrantStore()

    def query(self, user_query):
        """
        Executes the full RAG pipeline:
        1. Route query to section.
        2. Retrieve relevant chunks from selected section's collection.
        3. Generate answer using retrieved context.
        """
        
        # Step 1: Route Query
        print(f"Routing query: {user_query}")
        # Unpack 4 values now
        selected_section, score, explanation, all_scores = self.router.route_query(user_query)
        
        if score < 0.3:
            return {
                "answer": "I'm not confident about which section this query belongs to. Could you please rephrase?",
                "section": selected_section,
                "score": score,
                "explanation": explanation,
                "all_scores": all_scores,
                "context": []
            }
            
        print(f"Selected section: {selected_section} (Score: {score})")
        
        # Step 2: Retrieve Context from Selected Collection
        collection_name = Config.COLLECTIONS.get(selected_section)
        if not collection_name:
            return {
                "answer": f"Error: No collection found for section '{selected_section}'.",
                "section": selected_section,
                "score": score,
                "explanation": explanation,
                "all_scores": all_scores,
                "context": []
            }
            
        print(f"Searching in collection: {collection_name}")
        query_embedding = self.openai_client.get_embedding(user_query)
        # Search returns a list of ScoredPoint, need to access payload
        results = self.quadrant_store.search(collection_name, query_embedding, limit=3)
        
        context_chunks = [result.payload['text'] for result in results]
        context_text = "\n\n".join(context_chunks)
        
        # Step 3: Generate Answer
        print("Generating answer...")
        # Construct messages correctly for OpenAI client
        # OpenAIClient.get_completion expects messages list
        messages = [
            {"role": "system", "content": "You are a helpful documentation assistant. Answer the user's question based ONLY on the provided context. If the answer is not in the context, say 'Information not available in docs'."},
            {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {user_query}"}
        ]
        
        # Assuming OpenAIClient returns just the content string
        answer = self.openai_client.get_completion(messages)
        
        return {
            "answer": answer,
            "section": selected_section,
            "score": score,
            "explanation": explanation,
            "all_scores": all_scores,
            "context": context_chunks
        }
