# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import PyPDFLoader
# from pathlib import Path
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# from langchain_qdrant import QdrantVectorStore
# # from qdrant_client import QdrantClient


# # TODO: Step1: PDF Loader
# file_path = "C:\\Users\\user\\OneDrive\\Documents\\Generative_AI\\RAG\\Simple_RAG\\nodejs.pdf"
# loader = PyPDFLoader(file_path = file_path)
# docs = loader.load()   # List of docs(page1,page2,...)
# # print(docs)


# # TODO: Step2: Text Splitter for better embedding and retrieval bascially
# # As one page might contain huge data and there might be the case where context may loose
# # so making 1000-1000 chunks for having better retrival and processing 

# # overlap :- 200 means that last 200 characters of previous chunk will be 
# # repeated in next chunk for better context understanding and retrieval
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=100, chunk_overlap=20
#     )
# texts = text_splitter.split_text(docs[0].page_content)


# # Split the documents into chunks
# split_docs = text_splitter.split_documents(docs)

# # print("DOCS",len(docs))
# # print("Split",len(split_docs))


# # TODO: Step3: Embeddings
# # We will be using OpenAI's embedding model to convert text into vector representation
# embeddings = OpenAIEmbeddings(
#     model = "text-embedding-3-large",
#     api_key = os.getenv("OPENAI_API_KEY")  # Use environment variable
# )
# print(embeddings)


# # TODO: Step4: Vector Store(local qdrant)
# # Here embedding is been stored in vector database for better retrieval and processing
# # vector_store = QdrantVectorStore.from_documents(
# #     documents = [],
# #     url = "http://localhost:6333",
# #     collection_name = "learning_langchain",
# #     embedding=embeddings
# # )

# # vector_store.add_documents(documents = split_docs)
# print("Ingestion done...")



# # TODO: Retrieval 
# retriever = QdrantVectorStore.from_existing_collection(
#     url = "http://localhost:6333",
#     collection_name = "learning_langchain",
#     embedding = embeddings
# )


# # Vector embedding of this query is going to be compared with the vector embeddings of the chunks stored in qdrant and top 4 similar chunks will be retrieved

# relevant_chunks = retriever.similarity_search(
#     query = "What is FS module?", k = 4
#     )
# print("Relevant Chunks: ", relevant_chunks)


# SYSTEM_PROMPT = f"""You are a helpful assistant who answers strictly based on the provided context.

# Context:
# {relevant_chunks}
# """

# # ------------------------------------------------------------------------------------------------------------------
# # TODO: Step5: Pass retrieved context + user query to LLM

# # User query
# user_query = "What is FS module?"

# # Initialize Chat Model
# llm = ChatOpenAI(
#     model="gpt-4o-mini",   # fast and cost-efficient
#     api_key=os.getenv("OPENAI_API_KEY")  # Use environment variable
# )

# # Convert retrieved Document objects into readable text
# context_text = "\n\n".join([doc.page_content for doc in relevant_chunks])

# # Final prompt combining system instruction + context + user query
# final_prompt = f"""
# You are a helpful assistant who answers strictly based on the provided context.

# Context:
# {context_text}

# Question:
# {user_query}

# Answer:
# """

# # Generate response from LLM
# response = llm.invoke(final_prompt)

# # Print final answer
# print("\nLLM Answer:\n", response.content)











































from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore

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
    api_key="sk-xxxxxxxxxxxxxxxx"   # ← Put your real key
)

print("Embeddings loaded...")

# ------------------------------------------------------------------------------------------------------------------
# Step4: Ingestion (Run only first time)

# vector_store = QdrantVectorStore.from_documents(
#     documents=split_docs,
#     url="http://localhost:6333",
#     collection_name="learning_langchain",
#     embedding=embeddings
# )
# print("Ingestion done...")

# ------------------------------------------------------------------------------------------------------------------
# Step5: Retrieval

vector_store = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_langchain",
    embedding=embeddings
)

user_query = "What is FS module?"

relevant_chunks = vector_store.similarity_search(
    query=user_query,
    k=4
)

print("Relevant Chunks Retrieved:", len(relevant_chunks))

# Safety check
if len(relevant_chunks) == 0:
    print("No context found. Run ingestion first.")
    exit()

# ------------------------------------------------------------------------------------------------------------------
# Step6: Pass context to LLM

context_text = "\n\n".join([doc.page_content for doc in relevant_chunks])

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key="sk-xxxxxxxxxxxxxxxx"   # same key
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
