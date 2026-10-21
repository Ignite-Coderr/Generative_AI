# Multi-Query RAG with Reciprocal Rank Fusion (RRF)

## Project Overview
This project implements an advanced Retrieval-Augmented Generation (RAG) pipeline designed to overcome the limitations of single-query retrieval. By using **Multi-Query Transformation** and **Reciprocal Rank Fusion (RRF)**, the system captures different semantic nuances of a user's question, leading to more accurate and comprehensive answers.

## Architecture
![Architecture](architecture.png)

### The Workflow:
1.  **Original Question**: The user submits a query.
2.  **Multi-Query Generation**: An LLM generates 3 different versions of the query to cover various perspectives.
3.  **Vector Search**: Each query performs an independent search in the **Qdrant** vector database.
4.  **Reciprocal Rank Fusion (RRF)**: The results from all 3 searches are combined. The RRF algorithm calculates a new score for each document based on its rank across all searches, effectively "fusing" the results.
5.  **Final Answer**: The top fused documents are sent to the LLM as context to generate a final, high-quality response.

## Tech Stack
-   **LLM**: OpenAI (`gpt-4o-mini`)
-   **Vector Database**: Qdrant (Dockerized)
-   **Orchestration**: LangChain
-   **Interface**: Streamlit
-   **Embeddings**: OpenAI (`text-embedding-3-small`)

## Setup & Execution

### 1. Spin up the Database
Start the Qdrant vector store using Docker:
```powershell
docker-compose -f docker-compose.db.yml up -d
```

### 2. Index your Data
Ensure your PDF (e.g., `nodejs.pdf`) is in the `data/` folder, then run the indexing script:
```powershell
python index_pdf.py
```

### 3. Start the RAG Assistant
Launch the modern Streamlit chat interface:
```powershell
streamlit run app.py
```
*Alternatively, use the CLI version:* `python multi_query_rag.py`

## Project Structure
-   `app.py`: Streamlit chat interface with real-time status updates of the RAG steps.
-   `index_pdf.py`: Handles PDF loading, chunking, and indexing into Qdrant.
-   `multi_query_rag.py`: Core logic for query transformation and RRF.
-   `docker-compose.db.yml`: Docker configuration for the Qdrant service.
-   `data/`: Directory for source documents and your `.env` configuration.

---
*Created for the Generative AI Learning Journey.*
