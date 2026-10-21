from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

# Step 1: Load documents
documents = [
    "Python is a great programming language for data science.",
    "Laptops with high RAM and GPU are good for machine learning.",
    "JavaScript is popular for web development.",
    "MacBooks are preferred by many software engineers."
]

# Convert text to vector embeddings
embedding_model = OpenAIEmbeddings()

# Step 2: Store embeddings in FAISS vector store
vector_db = FAISS.from_texts(documents, embedding_model)

# Step 3: User query
query = "Which laptop is best for AI projects?"

# Step 4: Search for the most relevant document
search_result = vector_db.similarity_search(query, k=1)
print("Top result:", search_result[0].page_content)