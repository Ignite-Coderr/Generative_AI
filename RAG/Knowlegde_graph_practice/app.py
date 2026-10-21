# ================================
# Mem0 Story → Knowledge Graph
# Little Red Riding Hood Pipeline
# ================================

import os
from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ================================
# Load environment variables
# ================================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

NEO4J_URL = os.getenv("NEO4J_URL", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

USER_ID = "storybook_user"
COLLECTION_NAME = "storybook_memory"

# ================================
# Mem0 Configuration
# ================================
config = {
    "version": "v1.1",

    # Embeddings
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "text-embedding-3-small"
        },
    },

    # LLM
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "gpt-4o-mini"
        },
    },

    # Vector Store → Qdrant
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": QDRANT_HOST,
            "port": QDRANT_PORT,
            "collection_name": COLLECTION_NAME,
        },
    },

    # Graph Store → Neo4j
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": NEO4J_URL,
            "username": NEO4J_USERNAME,
            "password": NEO4J_PASSWORD,
        },
    },
}

# Initialize clients
memory = Memory.from_config(config)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

print(f"Connected to Qdrant: {QDRANT_HOST}:{QDRANT_PORT}")
print(f"Using collection: {COLLECTION_NAME}")
print(f"Connected to Neo4j: {NEO4J_URL}")

# ================================
# Step 1: Load PDF
# ================================
def load_story(path):
    print("Loading PDF...")
    loader = PyPDFLoader(path)
    docs = loader.load()
    return docs


# ================================
# Step 2: Chunk Text
# ================================
def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.split_documents(docs)


# ================================
# Step 3: Ingest into Mem0
# Stores:
# - Vectors → Qdrant
# - Entities → Neo4j
# ================================
def ingest_story(pdf_path):
    docs = load_story(pdf_path)
    chunks = chunk_documents(docs)

    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        try:
            memory.add(
                chunk.page_content,
                user_id=USER_ID,
                metadata={
                    "source": "little_red_riding_hood",
                    "chunk": i
                }
            )
            print(f"Stored chunk {i+1}")
        except Exception as e:
            print(f"Error storing chunk {i}: {e}")

    print("\nIngestion complete!")
    print("Check:")
    print("Qdrant → http://localhost:6333/dashboard")
    print("Neo4j → http://localhost:7474")


# ================================
# Step 4: Chat (Hybrid Retrieval)
# ================================
def chat(query):
    result = memory.search(query=query, user_id=USER_ID)

    memories = "\n".join(
        [m["memory"] for m in result.get("results", [])]
    )

    print("\nRetrieved Context:\n", memories)

    system_prompt = f"""
You are a story knowledge assistant.
Use the provided context to answer.

Context:
{memories}
"""

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )

    answer = response.choices[0].message.content

    # Save conversation
    memory.add(
        f"User: {query}\nAssistant: {answer}",
        user_id=USER_ID
    )

    return answer


# ================================
# CLI
# ================================
if __name__ == "__main__":

    PDF_PATH = "data/little_red_riding_hood.pdf"

    print("\n1. Ingest Story")
    print("2. Chat")
    choice = input("Select option: ")

    if choice == "1":
        ingest_story(PDF_PATH)

    elif choice == "2":
        while True:
            q = input("\n>> ")
            print("BOT:", chat(q))
