import os
import nltk
from dotenv import load_dotenv
from nltk.corpus import wordnet
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

# ------------------------------------------------------------------------------------------------------------------
# Download WordNet data (only once)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# ------------------------------------------------------------------------------------------------------------------
# Step1: PDF Loader
file_path = "nodejs.pdf"  # Adjusted to use the file in the current directory
loader = PyPDFLoader(file_path=file_path)
docs = loader.load()

# ------------------------------------------------------------------------------------------------------------------
# Step2: Text Splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
split_docs = text_splitter.split_documents(docs)

# ------------------------------------------------------------------------------------------------------------------
# Step3: Embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=os.getenv("OPENAI_API_KEY")
)

print("Embeddings loaded...")

# ------------------------------------------------------------------------------------------------------------------
# Step4: Ingestion (Check and run if collection doesn't exist or force run)
collection_name = "learning_langchain"
qdrant_url = "http://localhost:6333"

# Initialize Qdrant client to check if collection exists
client = QdrantClient(url=qdrant_url)
collection_exists = client.collection_exists(collection_name)

if not collection_exists:
    print(f"Collection '{collection_name}' not found. Creating and ingesting...")
    vector_store = QdrantVectorStore.from_documents(
        documents=split_docs,
        url=qdrant_url,
        collection_name=collection_name,
        embedding=embeddings
    )
    print("Ingestion done...")
else:
    print(f"Collection '{collection_name}' already exists. Skipping ingestion.")
    vector_store = QdrantVectorStore.from_existing_collection(
        url=qdrant_url,
        collection_name=collection_name,
        embedding=embeddings
    )

# ------------------------------------------------------------------------------------------------------------------
# Step5: Improved Retrieval with Query Expansion & Parallel Retrieval

user_query = "What is FS module?"

# ---- Query Expansion (Fan‑out) ----
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace('_', ' ')
            if synonym != word:
                synonyms.add(synonym)
    return list(synonyms)

def expand_query(query, max_expansions=3):
    """Generate query variants by replacing one word with a synonym."""
    words = query.split()
    variants = [query]  # include original
    for i, word in enumerate(words):
        syns = get_synonyms(word)
        # Take the first synonym for each word to keep total manageable
        for syn in syns[:1]:
            new_words = words.copy()
            new_words[i] = syn
            variants.append(' '.join(new_words))
            if len(variants) >= max_expansions + 1:
                return variants
    return variants[:max_expansions + 1]

expanded_queries = expand_query(user_query)
print(f"Original query: {user_query}")
print(f"Expanded queries: {expanded_queries}")

# ---- Parallel Retrieval (simulated sequentially) ----
K_PER_QUERY = 2   # retrieve 2 chunks per expanded query
unique_contents = set()
unique_docs = []

for q in expanded_queries:
    docs_for_q = vector_store.similarity_search(query=q, k=K_PER_QUERY)
    for doc in docs_for_q:
        # Use content as a simple deduplication key
        if doc.page_content not in unique_contents:
            unique_contents.add(doc.page_content)
            unique_docs.append(doc)

print(f"Unique chunks retrieved: {len(unique_docs)}")

# Safety check
if len(unique_docs) == 0:
    print("No context found. Run ingestion first.")
    exit()

# ------------------------------------------------------------------------------------------------------------------
# Step6: Pass context to LLM

context_text = "\n\n".join([doc.page_content for doc in unique_docs])

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

final_prompt = f"""
You are a helpful assistant who answers strictly based on the provided context.

Context:
{context_text}

Question:
{user_query}

Answer:
"""

response = llm.invoke(final_prompt)

print("\nLLM Answer:\n")
print(response.content)