import streamlit as st
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.pipeline import run_rag

st.title("Production Decomposition RAG")

query = st.text_input("Ask a question")

if st.button("Search"):
    answer, sub_queries = run_rag(query)

    st.write("Sub Queries:")
    for q in sub_queries:
        st.write("-", q)

    st.write("### Answer")
    st.write(answer)
