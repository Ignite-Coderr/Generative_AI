
import os
import chromadb
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 1. Setup Vector Database (ChromaDB)
print("--- Setting up ChromaDB ---")
client = chromadb.PersistentClient(path="./chroma_db_local")
collection = client.get_or_create_collection(name="practice_collection")

# 2. Add sample data
print("--- Adding documents to Vector DB ---")
documents = [
    "AGI (Artificial General Intelligence) is AI that can perform any intellectual task a human can.",
    "Vector Databases store data as high-dimensional vectors, allowing for similarity search.",
    "ChromaDB is an open-source vector database designed for AI applications.",
    "RAG (Retrieval-Augmented Generation) combines LLMs with external data retrieval."
]

# For simplicity, we use the documents as placeholders for embeddings if not using a real embedding model
# But here we'll just add them as documents and let Chroma handle simple indexing if we had an embedding function
# Since the user's notebook shows manual embeddings, we'll simulate that or use a simple mock.
# Notebook example: embeddings=[[0.1, 0.2, 0.3], ...]
collection.add(
    ids=["id1", "id2", "id3", "id4"],
    documents=documents,
    metadatas=[{"type": "definition"}, {"type": "database"}, {"type": "tool"}, {"type": "method"}]
)

# 3. Query the Vector DB
query_text = "What is AGI?"
results = collection.query(
    query_texts=[query_text],
    n_results=1
)
context = results['documents'][0][0]
print(f"Retrieved Context: {context}")

# 4. Use Euri API to answer based on context
print("\n--- Querying Euri API with Vector DB Context ---")
EURI_API_URL = "https://api.euron.one/api/v1/euri/chat/completions"
EURI_API_TOKEN = os.getenv("EURI_API_TOKEN")

payload = {
    "messages": [
        {
            "role": "system",
            "content": f"You are a helpful assistant. Use the following context to answer the user: {context}"
        },
        {
            "role": "user",
            "content": query_text
        }
    ],
    "model": "gpt-4.1-nano",
    "max_tokens": 500,
    "temperature": 0.7
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {EURI_API_TOKEN}"
}

try:
    response = requests.post(EURI_API_URL, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        res_json = response.json()
        answer = res_json['choices'][0]['message']['content']
        print(f"Euri Answer: {answer}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")
