import os
from dotenv import load_dotenv

# -----------------------------
# Load Environment
# -----------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# -----------------------------
# LangChain Imports
# -----------------------------
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore as Qdrant
from qdrant_client import QdrantClient
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# -----------------------------
# Qdrant Connection (Docker)
# -----------------------------
client = QdrantClient(host="localhost", port=6333)
embeddings = OpenAIEmbeddings()

# -----------------------------
# Step 1: Define Website Categories
# Each category → separate collection
# -----------------------------
URLS = {
    "preprocessing": [
        "https://scikit-learn.org/stable/modules/preprocessing.html"
    ],
    "model_selection": [
        "https://scikit-learn.org/stable/modules/cross_validation.html"
    ],
    "linear_model": [
        "https://scikit-learn.org/stable/modules/linear_model.html"
    ],
    "clustering": [
        "https://scikit-learn.org/stable/modules/clustering.html"
    ],
}

# -----------------------------
# Step 2: Chunking Strategy
# Recursive splitter keeps semantic meaning
# -----------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)


# -----------------------------
# Step 3: Load + Embed + Store
# Each category → its own collection
# -----------------------------
def create_collections():
    from qdrant_client.models import Distance, VectorParams
    
    for category, urls in URLS.items():
        print(f"\nCreating collection: {category}")

        documents = []
        for url in urls:
            loader = WebBaseLoader(url)
            docs = loader.load()
            documents.extend(docs)

        # Chunking
        chunks = text_splitter.split_documents(documents)

        # Create collection manually
        try:
            client.delete_collection(collection_name=category)
        except:
            pass
        
        # Create new collection
        client.create_collection(
            collection_name=category,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
        
        # Add documents to collection
        vector_store = Qdrant(
            client=client,
            collection_name=category,
            embedding=embeddings
        )
        
        vector_store.add_documents(chunks)

        print(f"{category} -> {len(chunks)} chunks stored")

# Uncomment first time
# create_collections()

# -----------------------------
# Step 4: Logical Router
# Rule-based (No LLM decision)
# -----------------------------
def logical_router(query: str):
    q = query.lower()

    if any(word in q for word in ["scale", "normalize", "standardize", "encode"]):
        return "preprocessing"

    elif any(word in q for word in ["cross validation", "grid search", "train test"]):
        return "model_selection"

    elif any(word in q for word in ["regression", "lasso", "ridge", "linear model"]):
        return "linear_model"

    elif any(word in q for word in ["kmeans", "cluster", "clustering", "dbscan"]):
        return "clustering"

    # default
    return "model_selection"



# -----------------------------
# Step 5: Query Reasoning (Chain-of-Thought Style)
# This step helps interpret user intent
# -----------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

reason_prompt = PromptTemplate(
    template="""
User Question: {query}

Step-by-step, identify:
1. Main topic
2. Keywords
3. User intent

Return a short reasoning summary.
""",
    input_variables=["query"]
)

def reason_query(query):
    response = llm.invoke(reason_prompt.format(query=query))
    return response.content


# -----------------------------
# Step 6: Retrieval + Answer
# -----------------------------
def answer_query(query):
    # Step 1: Reasoning
    reasoning = reason_query(query)
    print("\nQuery Reasoning:\n", reasoning)

    # Step 2: Logical Routing
    collection = logical_router(query)
    print("\nRouted to collection:", collection)

    # Step 3: Load Vector Store
    vector_store = Qdrant(
        client=client,
        collection_name=collection,
        embedding=embeddings
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    # Step 4: QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    result = qa_chain.invoke(query)

    print("\nAnswer:\n", result["result"])

# -----------------------------
# Step 7: CLI Interface
# -----------------------------
if __name__ == "__main__":
    while True:
        query = input("\nAsk a question (or type exit): ")
        if query.lower() == "exit":
            break
        answer_query(query)