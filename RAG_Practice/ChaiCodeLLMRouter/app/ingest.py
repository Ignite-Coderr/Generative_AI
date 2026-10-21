import os
import tiktoken
from .config import Config
from .openai_client import OpenAIClient
from .quadrant_store import QuadrantStore
from tqdm import tqdm

class IngestionPipeline:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.quadrant_store = QuadrantStore()
        
    def _chunk_text(self, text, chunk_size=500, overlap=100):
        """Splits text into chunks of specified size and overlap."""
        tokenizer = tiktoken.get_encoding("cl100k_base")
        tokens = tokenizer.encode(text)
        
        chunks = []
        for i in range(0, len(tokens), chunk_size - overlap):
            chunk_tokens = tokens[i:i + chunk_size]
            chunks.append(tokenizer.decode(chunk_tokens))
            
        return chunks

    def ingest_directory(self, data_dir: str):
        """Reads files from data directory and ingests them into Quadrant."""
        
        files_map = Config.COLLECTIONS
        
        for section, collection_name in files_map.items():
            file_path = os.path.join(data_dir, f"{section}.txt")
            if not os.path.exists(file_path):
                print(f"File {file_path} not found. Skipping.")
                continue
                
            print(f"Processing {section} ({collection_name})...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            chunks = self._chunk_text(content, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)
            
            embeddings = []
            metadatas = []
            
            print(f"Generating embeddings for {len(chunks)} chunks in {section}...")
            for i, chunk in enumerate(tqdm(chunks)):
                embedding = self.openai_client.get_embedding(chunk)
                if embedding:
                    embeddings.append(embedding)
                    metadatas.append({
                        "section": section,
                        "source": f"{section}.txt",
                        "chunk_id": i
                    })
            
            if embeddings:
                print(f"Creating collection {collection_name}...")
                self.quadrant_store.create_collection(collection_name)
                print(f"Upserting to {collection_name}...")
                self.quadrant_store.upsert_chunks(collection_name, chunks, metadatas, embeddings)
                
        print("Ingestion complete!")

if __name__ == "__main__":
    ingestor = IngestionPipeline()
    # Assuming run from project root, data is ./data
    ingestor.ingest_directory("./data")
