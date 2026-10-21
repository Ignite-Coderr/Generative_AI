# Section-Based Logical Routing RAG using Quadrant DB and OpenAI

This project demonstrates an intelligent documentation assistant that routes user queries to specific documentation sections before performing RAG. This approach improves accuracy and reduces hallucinations by narrowing the search context.

## 🏗️ Architecture

1.  **User Query:** The user asks a question via the Streamlit UI.
2.  **Semantic Routing:** The system embeds the query and compares it against pre-computed embeddings of section descriptions (HTML, Git, SQL, etc.).
3.  **Section Selection:** The most relevant section is selected.
4.  **Targeted Retrieval:** The system searches ONLY the Qdrant collection corresponding to the selected section.
5.  **Answer Generation:** Relevant chunks are retrieved and sent to OpenAI (GPT-4o-mini) to generate a precise answer.

## 🚀 Features

*   **Logical Routing:** Automatically detects if a query is about HTML, Git, SQL, Django, DevOps, or C++.
*   **Multi-Collection RAG:** Maintains separate vector collections for each documentation section.
*   **Explainable AI:** Provides reasoning for why a specific section was chosen.
*   **Clean UI:** Streamlit interface showing routing details, confidence scores, and retrieved context.

## 📂 Project Structure

```
section_router_rag/
├── data/               # Source documentation files
├── app/                # Application logic
│   ├── config.py       # Configuration settings
│   ├── section_router.py # Semantic routing logic
│   ├── quadrant_store.py # Qdrant vector DB interactions
│   ├── ingest.py       # Data ingestion script
│   ├── rag_pipeline.py # Main RAG pipeline
│   └── openai_client.py # OpenAI API wrapper
├── streamlit_app.py    # Web application
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
└── README.md           # This file
```

## 🛠️ Prerequisites

*   Python 3.10+
*   OpenAI API Key
*   Qdrant (running locally via Docker or cloud)

## 💻 Local Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/ChaiCodeLLMRouter.git
    cd ChaiCodeLLMRouter
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables:**
    Create a `.env` file in the root directory:
    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    QD_HOST=localhost
    QD_PORT=6333
    ```

4.  **Start Qdrant (using Docker):**
    ```bash
    docker run -p 6333:6333 qdrant/qdrant
    ```

5.  **Ingest Data:**
    ```bash
    python -m app.ingest
    ```

6.  **Run the App:**
    ```bash
    streamlit run streamlit_app.py
    ```

## 🐳 Docker Deployment

Build and run the entire application using Docker:

1.  **Build the image:**
    ```bash
    docker build -t quadrant-rag .
    ```

2.  **Run the container:**
    ```bash
    docker run -p 8501:8501 -e OPENAI_API_KEY=your_key quadrant-rag
    ```

## 🔮 Future Improvements

*   **Hybrid Search:** Combine keyword search with vector search for better precision.
*   **Re-ranking:** Implement a re-ranking step after retrieval to improve context quality.
*   **User Feedback:** Allow users to correct the routing decision to improve the router over time.
