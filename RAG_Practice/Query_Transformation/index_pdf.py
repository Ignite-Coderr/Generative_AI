import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct


# Load environment variables
# Check current dir and data dir
if os.path.exists("data/.env"):
    load_dotenv("data/.env")
else:
    load_dotenv()

# Settings
PDF_PATH = os.path.join("data", "nodejs.pdf")
if not os.path.exists(PDF_PATH):
    PDF_PATH = "nodejs.pdf" # Fallback
QDRANT_URL = "http://localhost:6333"
QDRANT_COLLECTION_NAME = "learning_langchain"
EMBEDDING_MODEL = "text-embedding-3-small"

# Initialize components
# text-embedding-3-small default size is 1536
EMBEDDING_SIZE = 1536 
embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
client = QdrantClient(url=QDRANT_URL)

def index_pdf():
    # 1. Load PDF
    if not os.path.exists(PDF_PATH):
        print(f"Error: {PDF_PATH} not found. Please ensure the file exists in the current directory.")
        return

    print(f"Loading {PDF_PATH}...")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    # 2. Split documents
    print("Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    # 3. Ensure collection exists in Qdrant
    collections = client.get_collections().collections
    exists = any(c.name == QDRANT_COLLECTION_NAME for c in collections)
    
    if not exists:
        print(f"Creating collection '{QDRANT_COLLECTION_NAME}'...")
        client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE),
        )
    else:
        print(f"Collection '{QDRANT_COLLECTION_NAME}' already exists.")

    # 4. Prepare and insert data
    print(f"Embedding and indexing {len(chunks)} chunks...")
    points = []
    for i, chunk in enumerate(chunks):
        vector = embeddings.embed_query(chunk.page_content)
        points.append(
            PointStruct(
                id=i,
                vector=vector,
                payload={
                    "text": chunk.page_content,
                    "metadata": chunk.metadata
                }
            )
        )

    # Upsert points
    client.upsert(collection_name=QDRANT_COLLECTION_NAME, points=points)
    print("PDF indexed successfully!")

if __name__ == "__main__":
    index_pdf()