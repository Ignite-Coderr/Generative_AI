# Query Decomposition RAG with Iterative Context Aggregation

A production-grade RAG system that breaks down complex user queries into simpler sub-queries, retrieves information iteratively, and builds a comprehensive context to generate grounded, accurate answers.

## 🚀 Features
- **Query Decomposition**: Uses LLMs to split complex questions into 3-4 granular search queries.
- **Iterative Retrieval**: Sequentially retrieves and summarizes context to prevent information loss.
- **Vector Storage**: Persistent storage using **Qdrant** (hosted in Docker).
- **Modern Tech Stack**: Built with LangChain, OpenAI, Streamlit, and Docker.
- **Streamlit UI**: Clean, interactive interface for querying and visualizing sub-queries.

## 🛠️ Architecture
1. **User Input**: Enter a complex question in the Streamlit UI.
2. **Decomposition**: LLM rewrites the question into multiple sub-queries.
3. **Retrieval**: For each sub-query, relevant document chunks are retrieved from Qdrant.
4. **Context Aggregation**: A running "Global Context" is updated and refined at each step.
5. **Final Answer**: LLM generates the final response based on the fully aggregated context.

## 📋 Prerequisites
- Python 3.10+
- Docker & Docker Compose
- OpenAI API Key

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Aman-Husain-123/Query-Decomposition-RAG-with-Iterative-Context-Aggregation.git
   cd Query-Decomposition-RAG-with-Iterative-Context-Aggregation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

4. **Start Qdrant (Docker)**:
   ```bash
   docker-compose up -d
   ```

## 🏃 Performance

1. **Index your Data**:
   Place your PDF in the `data/` folder and run:
   ```bash
   python run_indexing.py
   ```

2. **Run the App**:
   ```bash
   streamlit run ui/streamlit_app.py
   ```

## 📂 Project Structure
- `app/`: Core logic (decomposer, retriever, aggregator, pipeline).
- `ui/`: Streamlit interface.
- `data/`: Source documents for indexing.
- `docker-compose.yml`: Infrastructure for Qdrant.
- `run_indexing.py`: Helper script to build the vector store.
