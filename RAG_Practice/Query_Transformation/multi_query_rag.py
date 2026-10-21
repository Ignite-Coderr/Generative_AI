import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from qdrant_client import QdrantClient

# Load environment variables
if os.path.exists("data/.env"):
    load_dotenv("data/.env")
else:
    load_dotenv()

COLLECTION_NAME = "learning_langchain"

# LLM
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

# Embeddings
embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

# Qdrant
client = QdrantClient(url='http://localhost:6333')

# -----------------------------
# Step 1: Generate Multi Queries
# -----------------------------
def generate_multi_queries(question):
    prompt = f"""
Generate 3 different search queries for the following question to help retrieve relevant documents from a vector database.
Question: {question}

Return each query on a new line.
"""
    # Fix: Use invoke() instead of predict()
    response = llm.invoke(prompt)
    content = response.content if hasattr(response, 'content') else str(response)
    queries = [q.strip() for q in content.split("\n") if q.strip()]
    return queries[:3]

# -----------------------------
# Step 2: Retrieve for each query
# -----------------------------
def retrieve_for_query(query, top_k=5):
    vector = embeddings.embed_query(query)
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=top_k
    ).points
    return results

# -----------------------------
# Step 3: Reciprocal Rank Fusion
# -----------------------------
def rrf(results_list, k=60):
    scores = {}

    for results in results_list:
        for rank, res in enumerate(results):
            doc_id = res.id
            # Using point ID as the key for fusion
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)

    # Sort by score
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Fetch text
    final_docs = []
    for doc_id, _ in sorted_docs[:5]:
        point = client.retrieve(COLLECTION_NAME, ids=[doc_id])[0]
        final_docs.append(point.payload["text"])

    return final_docs

# -----------------------------
# Step 4: Answer Generation
# -----------------------------
def generate_answer(question, context_docs):
    context = "\n\n".join(context_docs)

    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{question}

Answer:
"""
    # Fix: Use invoke() instead of predict()
    response = llm.invoke(prompt)
    return response.content if hasattr(response, 'content') else str(response)

# -----------------------------
# Pipeline
# -----------------------------
def multi_query_rag(question):
    # Multi-query
    print(f"\nOriginal Question: {question}")
    queries = generate_multi_queries(question)
    print("Generated Queries:", queries)

    # Retrieve
    print("Retrieving documents for all queries...")
    results_list = [retrieve_for_query(q) for q in queries]

    # RRF
    print("Performing Reciprocal Rank Fusion...")
    docs = rrf(results_list)

    # Answer
    print("Generating final answer...")
    answer = generate_answer(question, docs)
    return answer

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    print(f"Connected to Qdrant at http://localhost:6333, Collection: {COLLECTION_NAME}")
    while True:
        try:
            q = input("\nAsk (type 'exit' to quit): ")
            if q.lower() == "exit":
                break
            ans = multi_query_rag(q)
            print("\nAnswer:", ans)
        except Exception as e:
            print(f"Error: {e}")
