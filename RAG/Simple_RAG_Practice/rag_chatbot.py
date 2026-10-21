"""
RAG Chatbot – Interactive Question Answering from Multiple Documents

Features:
- Loads all documents from a specified folder (supports .pdf, .txt, .md, etc.)
- Splits documents into chunks, creates embeddings (OpenAI), stores in Qdrant.
- Interactive chat loop: user asks questions, bot retrieves relevant chunks and answers.
- Only ingests documents if the Qdrant collection is empty (avoids re‑ingestion).
- Designed to run inside Docker together with Qdrant.

Environment Variables:
- OPENAI_API_KEY        : Your OpenAI API key (required)
- QDRANT_URL            : Qdrant URL (default: http://localhost:6333)
- DOCUMENTS_PATH        : Path to the folder containing documents (default: /data/documents)
- COLLECTION_NAME       : Qdrant collection name (default: "rag_collection")
- CHUNK_SIZE            : Number of characters per chunk (default: 1000)
- CHUNK_OVERLAP         : Overlap between chunks (default: 200)
- TOP_K                 : Number of chunks to retrieve (default: 4)
- LLM_MODEL             : OpenAI model name (default: "gpt-4o-mini")
- EMBEDDING_MODEL       : OpenAI embedding model (default: "text-embedding-3-large")
"""

import os
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ----------------------------------------------------------------------
# Configuration from environment variables
# ----------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

# Default to local 'DOCUMENTS_PATH' if not set
current_dir = Path(__file__).parent
DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH", str(current_dir / "DOCUMENTS_PATH"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "rag_collection")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
TOP_K = int(os.getenv("TOP_K", "4"))
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")


# ----------------------------------------------------------------------
# Helper: check if Qdrant collection exists
# ----------------------------------------------------------------------
def collection_exists(client: QdrantClient, collection_name: str) -> bool:
    """Return True if the collection exists, False otherwise."""
    try:
        client.get_collection(collection_name)
        return True
    except UnexpectedResponse:
        return False
    


# ----------------------------------------------------------------------
# Step 1-4: Load documents, split, embed, and store (ingestion)
# ----------------------------------------------------------------------
def ingest_documents():
    """Load all documents from DOCUMENTS_PATH, split, embed, and store in Qdrant."""
    print("[INFO] Loading documents...")
    if not Path(DOCUMENTS_PATH).exists():
        raise FileNotFoundError(f"Documents folder not found: {DOCUMENTS_PATH}")

    # Use DirectoryLoader to load .txt, .pdf, .md (you can add more glob patterns)
    loader = DirectoryLoader(
        DOCUMENTS_PATH,
        glob="**/*.*",                     # load all files – you can restrict to specific extensions
        show_progress=True,
        use_multithreading=True
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} document(s).")

    if not docs:
        print("[WARN] No documents found. Please add some files to the documents folder.")
        return

    print("[INFO] Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    split_docs = text_splitter.split_documents(docs)
    print(f"Created {len(split_docs)} chunks.")

    print("[INFO] Connecting to Qdrant...")
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )

    print("[INFO] Storing embeddings in Qdrant...")
    QdrantVectorStore.from_documents(
        documents=split_docs,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
        force_recreate=True,   # overwrite if collection already exists
    )
    print("[SUCCESS] Ingestion complete.\n")


# ----------------------------------------------------------------------
# Step 5-6: Interactive chat loop
# ----------------------------------------------------------------------
def chat_loop():
    """Retrieve relevant chunks for user queries and generate answers."""
    print("[INFO] Connecting to Qdrant for retrieval...")
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )

    vector_store = QdrantVectorStore.from_existing_collection(
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )

    llm = ChatOpenAI(
        model=LLM_MODEL,
        openai_api_key=OPENAI_API_KEY,
        temperature=0
    )

    print("\n[INFO] RAG Chatbot is ready! Ask me anything about your documents.")
    print("(Type 'quit' or 'exit' to stop)\n")

    while True:
        try:
            user_query = input("You: ").strip()
        except EOFError:
            break
            
        if user_query.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        if not user_query:
            continue

        print("[INFO] Searching for relevant context...")
        relevant_chunks = vector_store.similarity_search(user_query, k=TOP_K)

        if not relevant_chunks:
            print("[WARN] No relevant information found. Try another question.\n")
            continue

        # Combine chunk texts
        context_text = "\n\n".join([doc.page_content for doc in relevant_chunks])

        # Build the prompt (with strict instructions)
        final_prompt = f"""
You are a helpful assistant who answers strictly based on the provided context.
If the answer cannot be derived from the context, say "I don't have enough information to answer that."

Context:
{context_text}

Question:
{user_query}

Answer:
"""
        print("[INFO] Generating answer...")
        response = llm.invoke(final_prompt)
        print(f"\nBot: {response.content}\n")

# ----------------------------------------------------------------------
# Main: decide whether to ingest or directly start chat
# ----------------------------------------------------------------------
def main():
    # Quick check if the collection exists in Qdrant
    client = QdrantClient(url=QDRANT_URL)
    
    # Check if collection is empty
    should_ingest = False
    if not collection_exists(client, COLLECTION_NAME):
        print("[INFO] Collection does not exist. Starting ingestion...")
        should_ingest = True
    else:
        # Check if collection is empty
        collection_info = client.get_collection(COLLECTION_NAME)
        if collection_info.points_count == 0:
            print("[WARN] Collection exists but is empty. Starting ingestion...")
            should_ingest = True
        else:
            print(f"[INFO] Collection '{COLLECTION_NAME}' already exists with {collection_info.points_count} vectors. Skipping ingestion.\n")
            
    if should_ingest:
        ingest_documents()

    chat_loop()

if __name__ == "__main__":
    main()