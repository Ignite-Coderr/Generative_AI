from langchain.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from app.config import *

def retrieve(query):
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    embeddings = OpenAIEmbeddings()
    vector = embeddings.embed_query(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=TOP_K
    ).points

    return [r.payload["text"] for r in results]
