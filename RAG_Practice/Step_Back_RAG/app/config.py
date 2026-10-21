import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "pdf_docs"

EMBED_DIM = 1536
TOP_K = 3
SUB_QUERY_COUNT = 4
