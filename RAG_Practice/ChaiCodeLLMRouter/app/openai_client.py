from openai import OpenAI
import os
from .config import Config

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
    def get_embedding(self, text, model=None):
        """Generates an embedding for the given text."""
        model = model or Config.EMBEDDING_MODEL
        try:
            # Replace newlines with spaces for better results
            text = text.replace("\n", " ")
            return self.client.embeddings.create(input=[text], model=model).data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None

    def get_completion(self, messages, model=None):
        """Generates a chat completion."""
        model = model or Config.LLM_MODEL
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0  # For more deterministic answers
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating completion: {e}")
            return "Thinking..." # Fallback
