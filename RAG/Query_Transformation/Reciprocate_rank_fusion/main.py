import nltk
from nltk.corpus import wordnet
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore

# ------------------------------------------------------------------------------------------------------------------
# Download WordNet data (only once)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# ------------------------------------------------------------------------------------------------------------------
# Step1: PDF Loader
file_path = "C:\\Users\\user\\OneDrive\\Documents\\Generative_AI\\RAG\\Simple_RAG\\nodejs.pdf"
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
    api_key="sk-xxxxxxxxxxxxxxxx"   # ← Replace with your actual OpenAI API key
)

print("Embeddings loaded...")

# ------------------------------------------------------------------------------------------------------------------
# Step4: Ingestion (Run only first time)
# Uncomment the lines below to ingest documents into Qdrant.
# Make sure Qdrant is running at http://localhost:6333

# vector_store = QdrantVectorStore.from_documents(
#     documents=split_docs,
#     url="http://localhost:6333",
#     collection_name="learning_langchain",
#     embedding=embeddings
# )
# print("Ingestion done...")

# ------------------------------------------------------------------------------------------------------------------
# Step5: Retrieval with Query Expansion & Reciprocal Rank Fusion

# Connect to existing Qdrant collection
vector_store = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_langchain",
    embedding=embeddings
)

user_query = "What is FS module?"

# ---- Query Expansion (Fan‑out) using WordNet synonyms ----
def get_synonyms(word):
    """Return a list of synonyms for a given word (excluding the word itself)."""
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace('_', ' ')
            if synonym != word:
                synonyms.add(synonym)
    return list(synonyms)

def expand_query(query, max_expansions=3):
    """
    Generate query variants by replacing one word with its first synonym.
    Includes the original query. Returns at most max_expansions+1 variants.
    """
    words = query.split()
    variants = [query]  # always include original
    for i, word in enumerate(words):
        syns = get_synonyms(word)
        # Use the first synonym for each word to keep total manageable
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
K_PER_QUERY = 5          # number of chunks to retrieve per expanded query
all_rankings = []        # will hold list of (doc_id, rank) for each query
doc_store = {}           # maps doc_id (content) -> Document object

for q in expanded_queries:
    docs_for_q = vector_store.similarity_search(query=q, k=K_PER_QUERY)
    ranking = []
    for rank, doc in enumerate(docs_for_q, start=1):   # 1‑based rank
        # Use the page content as a simple unique identifier
        doc_id = doc.page_content
        ranking.append((doc_id, rank))
        if doc_id not in doc_store:
            doc_store[doc_id] = doc
    all_rankings.append(ranking)

# ---- Reciprocal Rank Fusion ----
def reciprocal_rank_fusion(rankings, k=60):
    """
    Combine multiple rankings using the RRF formula.
    rankings: list of lists of (doc_id, rank) where rank is 1‑based.
    Returns list of (doc_id, score) sorted descending by score.
    """
    scores = {}
    for ranking in rankings:
        for doc_id, rank in ranking:
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

rrf_results = reciprocal_rank_fusion(all_rankings, k=60)

# Select top N chunks after fusion
TOP_N = 4
final_docs = [doc_store[doc_id] for doc_id, _ in rrf_results[:TOP_N]]

print(f"Unique chunks after RRF: {len(final_docs)}")

# Safety check
if len(final_docs) == 0:
    print("No context found. Run ingestion first.")
    exit()

# ------------------------------------------------------------------------------------------------------------------
# Step6: Pass context to LLM (unchanged)

context_text = "\n\n".join([doc.page_content for doc in final_docs])

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key="sk-xxxxxxxxxxxxxxxx"   # same API key
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