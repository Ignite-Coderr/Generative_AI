"""
Streamlit Web Application for Intelligent Model Router

This application provides an interactive interface for:
- Entering user queries
- Visualizing routing decisions
- Displaying model responses
"""

import streamlit as st
from app.router import IntelligentRouter
from app.model_runner import ModelRunner
from app.utils import format_routing_analysis, calculate_confidence_level


# Page configuration
st.set_page_config(
    page_title="Intelligent Model Router",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        font-size: 1.1rem;
        border-radius: 8px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    h1 {
        color: #1f77b4;
    }
    .success-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_router():
    """Initialize and cache the router instance"""
    return IntelligentRouter()


def main():
    """Main application function"""
    
    # Header
    st.title("🤖 Intelligent Model Router")
    st.markdown("### AI-Powered Query Routing System")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 About")
        st.markdown("""
        This system intelligently routes your queries to the most appropriate AI model based on:
        
        - **Query Complexity**
        - **Intent Detection**
        - **Embedding Similarity**
        
        ### Available Models:
        
        🔢 **Small-Math**  
        Basic arithmetic operations
        
        🧮 **DeepSeek-Math**  
        Advanced mathematical reasoning
        
        📚 **Research-GPT**  
        Detailed explanations & research
        
        🎭 **Roast-GPT**  
        Creative & humorous responses
        """)
        
        st.markdown("---")
        st.markdown("**Built with:**")
        st.markdown("- Sentence Transformers")
        st.markdown("- FAISS Vector DB")
        st.markdown("- Streamlit")
    
    # Initialize router
    try:
        with st.spinner("🔄 Initializing router..."):
            router = initialize_router()
        st.success("✅ Router initialized successfully!")
    except Exception as e:
        st.error(f"❌ Error initializing router: {str(e)}")
        return
    
    # Main input section
    st.markdown("## 💬 Enter Your Query")
    
    # Query input
    query = st.text_area(
        "Type your question below:",
        height=100,
        placeholder="e.g., 'Explain transformer architecture' or '25 + 17' or 'Roast me!'"
    )
    
    # Example queries
    st.markdown("**Try these examples:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔢 2 + 3"):
            query = "2 + 3"
    
    with col2:
        if st.button("🧮 Solve equation"):
            query = "Solve the differential equation dy/dx = x^2"
    
    with col3:
        if st.button("📚 Explain AI"):
            query = "Explain transformer architecture in detail"
    
    with col4:
        if st.button("🎭 Roast me"):
            query = "Roast me"
    
    # Process query button
    if st.button("🚀 Route Query", type="primary"):
        if not query.strip():
            st.warning("⚠️ Please enter a query first!")
            return
        
        # Route the query
        with st.spinner("🔍 Analyzing query and routing to optimal model..."):
            try:
                routing_result = router.route(query)
                
                # Display results in columns
                st.markdown("---")
                st.markdown("## 📊 Routing Results")
                
                # Metrics row
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                
                with metric_col1:
                    st.metric(
                        "Selected Model",
                        routing_result['selected_model'],
                        delta=None
                    )
                
                with metric_col2:
                    similarity = routing_result['similarity_score']
                    confidence = calculate_confidence_level(similarity)
                    st.metric(
                        "Confidence Level",
                        confidence,
                        delta=f"{similarity:.2%}"
                    )
                
                with metric_col3:
                    model_info = routing_result['model_info']
                    st.metric(
                        "Model Complexity",
                        model_info.complexity.value.capitalize(),
                        delta=None
                    )
                
                # Routing Analysis
                st.markdown("### 🔍 Routing Analysis")
                
                analysis = routing_result['routing_analysis']
                formatted_analysis = format_routing_analysis(analysis)
                
                st.markdown(formatted_analysis)
                
                # Model Response Section
                st.markdown("---")
                st.markdown("## 🤖 Model Response")
                
                with st.spinner(f"⚡ Generating response using {routing_result['selected_model']}..."):
                    response = ModelRunner.run(
                        routing_result['selected_model'],
                        query
                    )
                
                # Display response in an attractive box
                st.markdown(f"""
                    <div class="success-box">
                        {response}
                    </div>
                """, unsafe_allow_html=True)
                
                # Additional model metadata
                with st.expander("📈 Model Metadata"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Model Name:** {model_info.name}")
                        st.markdown(f"**Complexity:** {model_info.complexity.value}")
                        st.markdown(f"**Cost Level:** {model_info.cost.value}")
                    
                    with col2:
                        st.markdown(f"**Latency:** {model_info.latency.value}")
                        st.markdown(f"**Similarity Score:** {similarity:.4f}")
                        st.markdown(f"**Description:** {model_info.description[:100]}...")
                
            except Exception as e:
                st.error(f"❌ Error processing query: {str(e)}")
                st.exception(e)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>Intelligent Model Router v1.0 | Built with ❤️ using Streamlit</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
