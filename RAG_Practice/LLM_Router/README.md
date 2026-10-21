# 🤖 Intelligent Model Router

An end-to-end AI system that intelligently routes user queries to the most appropriate AI model based on query complexity, intent, and semantic similarity using embeddings.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Docker Deployment](#docker-deployment)
- [Project Structure](#project-structure)
- [Examples](#examples)
- [Technical Details](#technical-details)

## 🎯 Overview

The Intelligent Model Router is a production-style system that analyzes incoming user queries and automatically selects the most suitable AI model to handle the request. This ensures optimal performance, cost-efficiency, and response quality.

### Why This Matters

Different queries require different computational approaches:
- Simple arithmetic doesn't need a heavy research model
- Complex mathematical proofs need specialized reasoning
- Explanatory queries benefit from detailed analysis models
- Creative requests work best with humor-focused models

This system automatically makes these decisions using **embedding-based semantic similarity** combined with **rule-based intent detection**.

## 🏗️ Architecture

```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│    Query Analysis Engine        │
│  ┌──────────────────────────┐   │
│  │ Intent Detection         │   │
│  │ Complexity Analysis      │   │
│  └──────────────────────────┘   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   Embedding-Based Routing       │
│  ┌──────────────────────────┐   │
│  │ Query → Embedding        │   │
│  │ FAISS Vector Search      │   │
│  │ Model Selection          │   │
│  └──────────────────────────┘   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│      Model Execution            │
│  ┌──────────────────────────┐   │
│  │ Small-Math               │   │
│  │ DeepSeek-Math            │   │
│  │ Research-GPT             │   │
│  │ Roast-GPT                │   │
│  └──────────────────────────┘   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────┐
│    Response     │
└─────────────────┘
```

## ✨ Features

### 🧠 Intelligent Routing
- **Embedding-based similarity search** using FAISS vector database
- **Intent detection** (arithmetic, mathematical, explanatory, creative)
- **Complexity analysis** (low, medium, high)
- **Confidence scoring** for routing decisions

### 🤖 Multi-Model Support
1. **Small-Math**: Fast arithmetic operations
2. **DeepSeek-Math**: Advanced mathematical reasoning
3. **Research-GPT**: Detailed explanations and analysis
4. **Roast-GPT**: Creative and humorous responses

### 📊 Transparent Decision Making
- Detailed routing analysis
- Similarity scores
- Human-readable explanations
- Model metadata display

### 🎨 User-Friendly Interface
- Clean Streamlit web application
- Interactive query examples
- Real-time routing visualization
- Comprehensive response display

## 🔧 How It Works

### 1. Model Registry
All available models are registered with metadata:

```python
Model(
    name="Small-Math",
    description="Specialized in basic arithmetic...",
    complexity=ComplexityLevel.LOW,
    cost=CostLevel.LOW,
    latency=LatencyLevel.LOW
)
```

### 2. Embedding Index Creation
Model descriptions are converted to embeddings using `sentence-transformers`:

```python
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embedding_model.encode(model_descriptions)
```

### 3. FAISS Vector Storage
Embeddings are stored in a FAISS index for fast similarity search:

```python
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
```

### 4. Query Processing
When a query arrives:
1. Analyze intent and complexity
2. Convert query to embedding
3. Search FAISS index for most similar model
4. Return selected model with confidence score

### 5. Response Generation
Execute the selected model and generate appropriate response.

## 🚀 Installation

### Prerequisites
- Python 3.10+
- pip package manager

### Local Setup

1. **Clone or navigate to the project directory:**
```bash
cd c:\Users\user\OneDrive\Documents\Generative_AI\RAG_Practice\LLM_Router
```

2. **Create virtual environment (recommended):**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Running the Application

```bash
streamlit run streamlit_app.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Interface

1. **Enter your query** in the text area
2. **Click "Route Query"** or use example buttons
3. **View routing analysis** including:
   - Selected model
   - Confidence level
   - Similarity score
   - Detailed explanation
4. **Read model response** tailored to your query

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t model-router .
```

### Run Container

```bash
docker run -p 8501:8501 model-router
```

Access the application at `http://localhost:8501`

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  model-router:
    build: .
    ports:
      - "8501:8501"
    environment:
      - PYTHONUNBUFFERED=1
```

Run with:
```bash
docker-compose up
```

## 📁 Project Structure

```
model_router/
│
├── app/
│   ├── __init__.py              # Package initialization
│   ├── model_registry.py        # Model definitions and metadata
│   ├── embedding_store.py       # FAISS vector store management
│   ├── router.py                # Core routing logic
│   ├── model_runner.py          # Model execution simulation
│   └── utils.py                 # Helper functions
│
├── streamlit_app.py             # Web application interface
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
└── README.md                    # This file
```

## 📚 Examples

### Example 1: Simple Arithmetic
**Query:** `2 + 3`

**Routing:**
- Model: Small-Math
- Intent: Arithmetic
- Complexity: Low
- Similarity: 0.85

**Response:** `Result: 5`

---

### Example 2: Advanced Math
**Query:** `Solve the differential equation dy/dx = x^2`

**Routing:**
- Model: DeepSeek-Math
- Intent: Mathematical
- Complexity: Medium
- Similarity: 0.78

**Response:** Step-by-step solution with mathematical reasoning

---

### Example 3: Explanation Request
**Query:** `Explain transformer architecture in detail`

**Routing:**
- Model: Research-GPT
- Intent: Explanatory
- Complexity: High
- Similarity: 0.82

**Response:** Comprehensive explanation with technical details

---

### Example 4: Creative Request
**Query:** `Roast me`

**Routing:**
- Model: Roast-GPT
- Intent: Creative
- Complexity: Low
- Similarity: 0.91

**Response:** Witty, humorous roast

## 🔬 Technical Details

### Embedding Model
- **Model:** `all-MiniLM-L6-v2` from sentence-transformers
- **Dimension:** 384
- **Metric:** L2 distance converted to similarity score

### Vector Database
- **Technology:** FAISS (Facebook AI Similarity Search)
- **Index Type:** IndexFlatL2
- **Search Method:** Exact nearest neighbor

### Intent Detection
Rule-based classification using keyword matching:
- Arithmetic: `\d+\s*[\+\-\*/]\s*\d+`
- Mathematical: `solve`, `equation`, `derivative`, etc.
- Explanatory: `explain`, `describe`, `what is`, etc.
- Creative: `roast`, `joke`, `funny`, etc.

### Complexity Analysis
Multi-factor analysis based on:
- Keyword presence (high/medium/low complexity keywords)
- Arithmetic pattern detection
- Query length (word count)

### Similarity Calculation
```python
similarity = exp(-distance / 10)
```
Converts L2 distance to 0-1 similarity score.

## 🛡️ Error Handling

The system includes robust error handling:
- Safe arithmetic evaluation (limited to basic operators)
- Model initialization validation
- Query processing exception handling
- Graceful fallbacks for edge cases

## 🎓 Learning Objectives

This project demonstrates:
- ✅ Embedding-based routing
- ✅ Vector database usage (FAISS)
- ✅ Modular code architecture
- ✅ Production-style error handling
- ✅ Clean UI/UX design
- ✅ Docker containerization
- ✅ Separation of concerns (logic vs. interface)

## 🤝 Contributing

This is a practice/educational project. Feel free to:
- Extend with actual model APIs
- Add more sophisticated routing logic
- Implement caching mechanisms
- Add monitoring and logging
- Create unit tests

## 📝 License

This project is for educational purposes.

## 👨‍💻 Author

Built as a demonstration of intelligent AI model routing using embeddings and vector databases.

---

**Note:** This is a simulation project. In production, you would:
- Replace simulated models with actual API calls
- Implement token counting and cost tracking
- Add authentication and rate limiting
- Include comprehensive logging and monitoring
- Implement caching for frequently asked queries
- Add A/B testing for routing strategies
