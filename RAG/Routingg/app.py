# ===============================
# Logical Routing RAG (Production)
# ===============================

import os
from fastapi import FastAPI
from dotenv import load_dotenv
from collections import defaultdict

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import Qdrant

from qdrant_client import QdrantClient


# ===============================
# Setup
# ===============================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

app = FastAPI()

# Models
embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Qdrant client
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


# ===============================
# Website Sections (Collections)
# ===============================

BASE = "https://docs.chaicode.com/youtube/"

SECTIONS = {
    "getting-started": BASE + "getting-started/",
    "html": BASE + "chai-aur-html/",
    "git": BASE + "chai-aur-git/",
    "cpp": BASE + "chai-aur-cpp/",
    "django": BASE + "chai-aur-django/",
    "sql": BASE + "chai-aur-sql/",
    "devops": BASE + "chai-aur-devops/",
}


# ===============================
# Helper: Check Collection
# ===============================
def collection_exists(name: str):
    collections = client.get_collections().collections
    return name in [c.name for c in collections]


# ===============================
# Ingest Website Section
# ===============================
def ingest_section(name, url):
    if collection_exists(name):
        print(f"Already exists: {name}")
        return

    print(f"Ingesting: {name}")

    loader = WebBaseLoader(url)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    splits = splitter.split_documents(docs)

    Qdrant.from_documents(
        splits,
        embeddings,
        url=f"http://{QDRANT_HOST}:{QDRANT_PORT}",
        collection_name=name,
    )

    print(f"Ingested: {name}")


# ===============================
# Bulk Ingest Endpoint
# ===============================
@app.post("/ingest")
def ingest_all():
    for name, url in SECTIONS.items():
        ingest_section(name, url)
    return {"status": "All sections ingested"}


# ===============================
# Logical Router (LLM)
# ===============================
def route_query(query: str):

    prompt = f"""
Route the user query to the most relevant category.

Categories:
{list(SECTIONS.keys())}

Query: {query}

Return only one category name.
"""

    category = llm.invoke(prompt).content.strip().lower()

    if category not in SECTIONS:
        category = "getting-started"

    return category


# ===============================
# Query Decomposition
# ===============================
def decompose_query(query: str):

    prompt = f"""
Rewrite this into 3 search queries:

Query: {query}

Return each on a new line.
"""

    text = llm.invoke(prompt).content

    queries = [
        q.strip("- ").strip()
        for q in text.split("\n")
        if q.strip()
    ]

    return queries[:3]


# ===============================
# Retriever (FIXED)
# ===============================
def get_retriever(collection_name: str):

    vectorstore = Qdrant.from_existing_collection(
        collection_name=collection_name,
        embedding=embeddings,
        url=f"http://{QDRANT_HOST}:{QDRANT_PORT}"
    )

    return vectorstore.as_retriever(search_kwargs={"k": 4})


# ===============================
# Reciprocal Rank Fusion
# ===============================
def rrf(results, k=60):
    scores = defaultdict(float)
    doc_map = {}

    for docs in results:
        for rank, doc in enumerate(docs):
            key = doc.page_content
            scores[key] += 1 / (rank + k)
            doc_map[key] = doc

    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [doc_map[text] for text, _ in sorted_docs[:5]]


# ===============================
# Ask Endpoint
# ===============================
@app.post("/ask")
def ask(query: str):

    # 1. Route to collection
    collection = route_query(query)

    # 2. Decompose
    sub_queries = decompose_query(query)

    # 3. Retrieve
    retriever = get_retriever(collection)
    results = [retriever.get_relevant_documents(q) for q in sub_queries]

    # 4. Rank Fusion
    fused_docs = rrf(results)

    context = "\n\n".join([doc.page_content for doc in fused_docs])

    # 5. Final Answer
    prompt = f"""
Answer the question using ONLY the context.

Context:
{context}

Question: {query}
"""

    answer = llm.invoke(prompt).content

    # 6. Sources
    sources = [
        {
            "source": doc.metadata.get("source", "web"),
            "content_preview": doc.page_content[:300]
        }
        for doc in fused_docs
    ]

    return {
        "routed_collection": collection,
        "sub_queries": sub_queries,
        "answer": answer,
        "sources": sources
    }
