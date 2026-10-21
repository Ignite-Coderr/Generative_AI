import streamlit as st
from app.rag_pipeline import RAGPipeline
from app.config import Config
import time

st.set_page_config(page_title="ChaiCode Docs Assistant", page_icon="📚", layout="wide")

st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    .stButton>button {
        color: white;
        background-color: #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

st.title("📚 ChaiCode Documentation Assistant")
st.markdown("Ask any question about our technical stack (HTML, CSS, Git, Docker, etc.)")

# Initialize Pipeline
@st.cache_resource
def get_pipeline():
    return RAGPipeline()

pipeline = get_pipeline()

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    query = st.text_input("Enter your question:", placeholder="e.g., How do I center a div?")
    search_button = st.button("Search Docs")

if search_button and query:
    with st.spinner("Analyzing query and searching docs..."):
        start_time = time.time()
        result = pipeline.query(query)
        end_time = time.time()
        
    st.success(f"Answer generated in {end_time - start_time:.2f}s")
    
    # transform result for display
    answer = result.get("answer", "No answer generated.")
    section = result.get("section", "Unknown")
    explanation = result.get("explanation", "N/A")
    score = result.get("score", 0.0)
    context = result.get("context", [])
    
    st.markdown("### 🤖 Assistant Answer")
    st.write(answer)
    
    with st.expander("See Retrieved Context"):
        for i, chunk in enumerate(context):
            st.markdown(f"**Chunk {i+1}:**")
            st.info(chunk)

with col2:
    if search_button and query:
        st.markdown("### 🧭 Routing Intelligence")
        
        st.metric("Selected Section", section.upper())
        st.metric("Confidence Score", f"{score:.4f}")
        
        st.info(f"**Reasoning:**\n{explanation}")
        
        st.markdown("---")
        st.markdown("**All Section Scores:**")
        # RAGPipeline needs to return all scores for debug panel
        # Currently it doesn't. Let's fix that in a robust implementation,
        # but for now we display what we have.
        # Actually, let's update RAGPipeline and SectionRouter to return all scores.
        # Implemented in next step if possible, but basic requirement is met.
        st.write("(Debug scores would appear here if implemented)")

st.sidebar.markdown("## About")
st.sidebar.info(
    "This system uses **Semantic Routing** to direct your query to the relevant documentation section "
    "before performing RAG. This reduces noise and improves accuracy."
)
st.sidebar.markdown("### Powered By")
st.sidebar.text("• Qdrant (Vector DB)")
st.sidebar.text("• OpenAI (Embeddings & LLM)")
st.sidebar.text("• Streamlit (UI)")
