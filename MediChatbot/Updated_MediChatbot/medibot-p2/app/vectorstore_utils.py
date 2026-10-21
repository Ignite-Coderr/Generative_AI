import openai
import chromadb
from typing import List
from app.config import OPENAI_EMBEDDING_BASE, OPENAI_EMBEDDING_KEY, EMBEDDING_MODEL, CHROMA_CONFIG
from app.pdf_utils import clean_text

# Configure OpenAI for standard embeddings API
openai.api_base = OPENAI_EMBEDDING_BASE
openai.api_key = OPENAI_EMBEDDING_KEY

def get_chroma_client():
    """Get ChromaDB cloud client"""
    if not CHROMA_CONFIG['api_key'] or not CHROMA_CONFIG['tenant']:
        print("⚠️ ChromaDB credentials not configured, using local storage")
        return None
    
    return chromadb.CloudClient(
        api_key=CHROMA_CONFIG['api_key'],
        tenant=CHROMA_CONFIG['tenant'],
        database=CHROMA_CONFIG['database']
    )

def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Get embeddings for texts using OpenAI API"""
    try:
        # Use OpenAI client for embeddings
        response = openai.Embedding.create(
            model=EMBEDDING_MODEL,
            input=texts
        )
        
        if hasattr(response, 'data') and isinstance(response.data, list):
            embeddings = [item.embedding for item in response.data]
            return embeddings
        else:
            print("❌ Invalid response format from OpenAI embeddings API")
            return []
            
    except Exception as e:
        print(f"❌ Error getting embeddings from OpenAI: {e}")
        return []

def create_chroma_collection(texts: List[str], batch_size: int = 10):
    """Create ChromaDB collection and store documents in batches"""
    try:
        pass
        
        # Ensure collection exists and is not soft deleted
        collection = ensure_collection_exists()
        if not collection:
            return None
        
        # Process documents in batches
        total_stored = 0
        for i in range(0, len(texts), batch_size):
            batch_texts = [clean_text(text) for text in texts[i:i + batch_size]]
            batch_num = (i // batch_size) + 1
            total_batches = (len(texts) + batch_size - 1) // batch_size
            
            print(f"🧠 Processing batch {batch_num}/{total_batches} ({len(batch_texts)} documents)...")
            
            # Get embeddings for this batch
            embeddings = get_embeddings(batch_texts)
            
            if not embeddings:
                print(f"❌ Failed to get embeddings for batch {batch_num}, skipping...")
                continue
            
            if len(embeddings) != len(batch_texts):
                print(f"⚠️  Warning: Got {len(embeddings)} embeddings for {len(batch_texts)} texts in batch {batch_num}")
                # Truncate to match
                min_len = min(len(embeddings), len(batch_texts))
                embeddings = embeddings[:min_len]
                batch_texts = batch_texts[:min_len]
            
            # Prepare documents for storage
            batch_ids = [f"doc_{i+j}_{hash(text[:50])}" for j, text in enumerate(batch_texts)]
            
            # Add documents to collection
            print(f"💾 Storing batch {batch_num} ({len(batch_texts)} documents) in ChromaDB...")
            collection.add(
                documents=batch_texts,
                embeddings=embeddings,
                ids=batch_ids
            )
            
            total_stored += len(batch_texts)
            print(f"✅ Batch {batch_num} stored successfully. Total stored: {total_stored}")
        
            print(f"🎉 Successfully stored {total_stored}/{len(texts)} documents in ChromaDB collection '{CHROMA_CONFIG['collection']}'")
            return collection
        
    except Exception as e:
        print(f"❌ Error creating ChromaDB collection: {e}")
        import traceback
        traceback.print_exc()
        return None

def clear_chroma_collection():
    """Clear all documents from ChromaDB collection"""
    try:
        client = get_chroma_client()
        if not client:
            print("⚠️ ChromaDB not configured")
            return False
            
        try:
            # Try to get the collection first
            collection = client.get_collection(CHROMA_CONFIG['collection'])
            # Delete the collection
            client.delete_collection(CHROMA_CONFIG['collection'])
            print(f"🗑️  Cleared ChromaDB collection '{CHROMA_CONFIG['collection']}'")
        except Exception as e:
            print(f"📂 Collection '{CHROMA_CONFIG['collection']}' doesn't exist or is already empty: {e}")
        return True
    except Exception as e:
        print(f"❌ Error clearing ChromaDB collection: {e}")
        return False

def ensure_collection_exists():
    """Ensure ChromaDB collection exists and is not soft deleted"""
    try:
        client = get_chroma_client()
        if not client:
            print("⚠️ ChromaDB not configured, using local fallback")
            return None
            
        try:
            # Try to get existing collection
            collection = client.get_collection(CHROMA_CONFIG['collection'])
            print(f"📂 Using existing collection: {CHROMA_CONFIG['collection']}")
            return collection
        except Exception as e:
            print(f"📂 Collection doesn't exist or is soft deleted: {e}")
            # Create new collection
            collection = client.create_collection(CHROMA_CONFIG['collection'])
            print(f"📂 Created new collection: {CHROMA_CONFIG['collection']}")
            return collection
    except Exception as e:
        print(f"❌ Error ensuring collection exists: {e}")
        return None

def retrieve_relevant_docs(query: str, k: int = 10):
    """Retrieve relevant documents from ChromaDB"""
    try:
        # Ensure collection exists
        collection = ensure_collection_exists()
        if not collection:
            print("❌ Failed to ensure collection exists for retrieval")
            return []
        
        # Get query embedding
        query_embeddings = get_embeddings([query])
        
        if not query_embeddings:
            print("Failed to get query embedding")
            return []
        
        # Ensure we have a valid embedding
        if not query_embeddings[0]:
            print("Empty query embedding")
            return []
        
        # Search for similar documents
        results = collection.query(
            query_embeddings=query_embeddings,
            n_results=k
        )
        
        # Format results for compatibility
        documents = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                # Create a document-like object for compatibility
                class Document:
                    def __init__(self, content):
                        self.page_content = content
                
                documents.append(Document(doc))
        
        return documents
        
    except Exception as e:
        print(f"Error retrieving documents from ChromaDB: {e}")
        return []

# Legacy function names for compatibility
def create_faiss_index(texts: List[str]):
    """Legacy function name - now uses ChromaDB"""
    return create_chroma_collection(texts)

def retrive_relevant_docs(vectorstore, query: str, k: int = 10):
    """Legacy function name - now uses ChromaDB"""
    return retrieve_relevant_docs(query, k)


