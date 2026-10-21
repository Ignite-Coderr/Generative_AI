import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from qdrant_client import QdrantClient

# Page configuration
st.set_page_config(page_title="Multi-Query RAG Assistant", page_icon="🤖", layout="wide")

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .stChatFloatingInputContainer {
        padding-bottom: 2rem;
    }
    .query-box {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# Load environment variables
if os.path.exists("data/.env"):
    load_dotenv("data/.env")
else:
    load_dotenv()

# Sidebar configuration
with st.sidebar:
    st.title("Settings")
    qdrant_url = st.text_input("Qdrant URL", value="http://localhost:6333")
    collection_name = st.text_input("Collection Name", value="learning_langchain")
    model_name = st.selectbox("LLM Model", ["gpt-4o-mini", "gpt-4o"], index=0)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.0)
    
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# Initialize components
@st.cache_resource
def get_llm(model, temp):
    return ChatOpenAI(model=model, temperature=temp)

@st.cache_resource
def get_embeddings():
    return OpenAIEmbeddings(model='text-embedding-3-small')

@st.cache_resource
def get_qdrant_client(url):
    return QdrantClient(url=url)

llm = get_llm(model_name, temperature)
embeddings = get_embeddings()
client = get_qdrant_client(qdrant_url)

# RAG Functions
def generate_multi_queries(question):
    prompt = f"""
Generate 3 different search queries for the following question to help retrieve relevant documents from a vector database.
Question: {question}

Return each query on a new line.
"""
    response = llm.invoke(prompt)
    content = response.content if hasattr(response, 'content') else str(response)
    queries = [q.strip() for q in content.split("\n") if q.strip()]
    return queries[:3]

def retrieve_for_query(query, collection, top_k=5):
    vector = embeddings.embed_query(query)
    results = client.query_points(
        collection_name=collection,
        query=vector,
        limit=top_k
    ).points
    return results

def rrf(results_list, collection, k=60):
    scores = {}
    for results in results_list:
        for rank, res in enumerate(results):
            doc_id = res.id
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)

    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    final_docs = []
    for doc_id, _ in sorted_docs[:5]:
        point = client.retrieve(collection, ids=[doc_id])[0]
        final_docs.append(point.payload["text"])
    return final_docs

def generate_answer(question, context_docs):
    context = "\n\n".join(context_docs)
    prompt = f"Answer the question using ONLY the context below.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    response = llm.invoke(prompt)
    return response.content if hasattr(response, 'content') else str(response)

# Chat Interface
st.title("🤖 Multi-Query RAG Assistant")
st.markdown("Ask questions about your indexed documents. This assistant uses **Multi-Query Retrieval** and **Reciprocal Rank Fusion (RRF)** for better accuracy.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("Thinking...", expanded=False) as status:
            # Step 1: Multi-query
            st.write("🔍 Generating alternative queries...")
            queries = generate_multi_queries(prompt)
            for q in queries:
                st.write(f"- *{q}*")
            
            # Step 2: Retrieve
            st.write("📥 Retrieving documents...")
            results_list = [retrieve_for_query(q, collection_name) for q in queries]
            
            # Step 3: RRF
            st.write("⚖️ Performing Reciprocal Rank Fusion...")
            docs = rrf(results_list, collection_name)
            
            # Step 4: Answer
            st.write("✍️ Generating final answer...")
            answer = generate_answer(prompt, docs)
            status.update(label="Response Complete", state="complete")
        
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
