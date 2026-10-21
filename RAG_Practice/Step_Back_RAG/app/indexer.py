from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from app.config import *

def index_pdf(pdf_path):
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    embeddings = OpenAIEmbeddings()

    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE)
    )

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    texts = [chunk.page_content for chunk in chunks]
    vectors = embeddings.embed_documents(texts)

    points = [
        PointStruct(
            id=i,
            vector=vector,
            payload={"text": text}
        )
        for i, (vector, text) in enumerate(zip(vectors, texts))
    ]

    client.upsert(collection_name=COLLECTION_NAME, points=points)

    print("Indexing completed.")
