import os
import logging
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Qdrant
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models

# Load environment variables from .env file if present
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Query Decomposition RAG")

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "nodejs_docs"
PDF_PATH = "data/nodejs.pdf"

# Initialize LLM and embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)

# Qdrant client
qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Vector store (lazy loaded)
vectorstore = None


def get_vectorstore():
    """Return the Qdrant vector store, initializing it if needed."""
    global vectorstore
    if vectorstore is None:
        # Check if collection exists, if not, ingest the PDF
        collections = qdrant_client.get_collections().collections
        if COLLECTION_NAME not in [c.name for c in collections]:
            logger.info("Collection not found. Starting ingestion...")
            ingest_pdf()
        vectorstore = Qdrant(
            client=qdrant_client,
            collection_name=COLLECTION_NAME,
            embeddings=embeddings,
        )
    return vectorstore


def ingest_pdf():
    """Load PDF, split into chunks, and index into Qdrant."""
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF not found at {PDF_PATH}")

    logger.info(f"Loading PDF from {PDF_PATH}")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    # Create collection (if not exists) with proper vector size for OpenAI embeddings
    try:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=qdrant_models.VectorParams(
                size=1536,  # OpenAI embedding dimension
                distance=qdrant_models.Distance.COSINE,
            ),
        )
        logger.info(f"Collection '{COLLECTION_NAME}' created.")
    except Exception as e:
        # Collection might already exist; ignore
        logger.info(f"Collection might already exist: {e}")

    # Add documents to the vector store
    Qdrant.from_documents(
        docs,
        embeddings,
        client=qdrant_client,
        collection_name=COLLECTION_NAME,
    )
    logger.info(f"Ingested {len(docs)} chunks into Qdrant.")


# ---------- Prompt Templates ----------
DECOMPOSE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in Node.js. Given a user question, break it down into a series of sub-questions that, when answered, will provide a comprehensive answer to the original question. The sub-questions should be specific and focused on different aspects. Return the sub-questions as a numbered list, each on a new line. Do not include any other text."),
    ("human", "{query}")
])

ANSWER_SUBQUESTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in Node.js. Use the following pieces of retrieved context to answer the sub-question. If you don't know the answer, just say you don't know. Keep the answer concise.\n\nContext: {context}"),
    ("human", "Sub-question: {sub_question}\n\nPrevious answers (for reference): {previous_answers}")
])

FINAL_ANSWER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in Node.js. Given the original user query and a set of intermediate answers to sub-questions, synthesize a comprehensive final answer. Provide a detailed and accurate response."),
    ("human", "Original query: {original_query}\n\nIntermediate answers:\n{intermediate_answers}")
])


def decompose_query(query: str) -> List[str]:
    """Use LLM to break down the query into a list of sub-questions."""
    chain = DECOMPOSE_PROMPT | llm | StrOutputParser()
    result = chain.invoke({"query": query})
    # Parse numbered list (simple parsing)
    lines = result.strip().split('\n')
    sub_questions = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Remove leading numbers, bullets, etc.
        if line[0].isdigit() and '. ' in line:
            line = line.split('. ', 1)[1]
        elif line.startswith('- ') or line.startswith('* '):
            line = line[2:]
        sub_questions.append(line)
    return sub_questions


def answer_sub_question(sub_question: str, previous_answers: str, retriever) -> str:
    """Retrieve context for a sub‑question and generate an answer."""
    docs = retriever.invoke(sub_question)
    context = "\n\n".join([doc.page_content for doc in docs])
    chain = ANSWER_SUBQUESTION_PROMPT | llm | StrOutputParser()
    return chain.invoke({
        "sub_question": sub_question,
        "context": context,
        "previous_answers": previous_answers
    })


def answer_query(query: str) -> str:
    """Main RAG pipeline with query decomposition."""
    # 1. Decompose the query into sub‑questions
    sub_questions = decompose_query(query)
    logger.info(f"Decomposed into {len(sub_questions)} sub‑questions: {sub_questions}")

    # 2. Prepare retriever
    retriever = get_vectorstore().as_retriever(search_kwargs={"k": 4})

    # 3. Answer each sub‑question sequentially, accumulating previous answers
    intermediate_answers = []
    previous = ""
    for i, sq in enumerate(sub_questions, 1):
        logger.info(f"Answering sub‑question {i}: {sq}")
        ans = answer_sub_question(sq, previous, retriever)
        formatted = f"Q{i}: {sq}\nA{i}: {ans}"
        intermediate_answers.append(formatted)
        previous += formatted + "\n\n"

    # 4. Synthesize final answer
    final_chain = FINAL_ANSWER_PROMPT | llm | StrOutputParser()
    final_answer = final_chain.invoke({
        "original_query": query,
        "intermediate_answers": "\n\n".join(intermediate_answers)
    })
    return final_answer


# ---------- API Models ----------
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

class IngestResponse(BaseModel):
    message: str


# ---------- API Endpoints ----------
@app.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest):
    """Ask a question using query decomposition RAG."""
    try:
        answer = answer_query(request.query)
        return QueryResponse(answer=answer)
    except Exception as e:
        logger.exception("Error in /ask")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest", response_model=IngestResponse)
async def ingest():
    """Force re‑ingestion of the PDF (recreates the collection)."""
    try:
        # Delete existing collection if it exists
        try:
            qdrant_client.delete_collection(COLLECTION_NAME)
            logger.info(f"Deleted collection '{COLLECTION_NAME}'")
        except Exception:
            pass  # Collection may not exist
        ingest_pdf()
        return IngestResponse(message="PDF ingested successfully.")
    except Exception as e:
        logger.exception("Error in /ingest")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)