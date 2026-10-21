# 🚀 Generative AI Learning Journey

A comprehensive collection of projects, experiments, and implementations exploring various aspects of Generative AI, LangChain, RAG systems, and AI agents.

## 📚 Repository Structure

```
GenerativeAI_Learning_Journey/
├── Agents/                          # LangChain Agents with Euron AI
├── agent_ui/                        # Agent UI implementations
├── API_Example/                     # API testing examples
├── API_Testing/                     # API testing utilities
├── Assignments/                     # Course assignments
├── Data_Preprocessing/              # Text preprocessing examples
├── Example2/                        # Additional examples
├── FASTAPI/                         # FastAPI implementations
├── FASTAPI_WITH_DATABASE/           # FastAPI with database integration
├── Internsip_Job_Scrapper/         # Job scraping project
├── Langchain/                       # LangChain experiments
├── lc312/                          # LangChain 3.12 examples
├── MediChatbot/                    # Medical chatbot with RAG
├── MediChatUtils/                  # Medical chat utilities
├── MediPDF_Processor/              # PDF processing for medical docs
├── MediVectorStore/                # Vector store for medical data
├── Model_Serving_On_Cloud/         # Cloud deployment examples
├── Mongo_DB/                       # MongoDB integrations
├── test_vibe/                      # Testing utilities
└── vector_db/                      # Vector database implementations
```

## 🎯 Featured Projects

### 1. **LangChain Agents** (`Agents/`)
Advanced agent implementations using LangChain 1.x and Euron AI.

**Features:**
- ✅ LangChain 1.x compatible
- ✅ Custom tools (calculator, string operations)
- ✅ Conversation memory with `InMemoryChatMessageHistory`
- ✅ LangGraph integration for modern agents
- ✅ LCEL (LangChain Expression Language) chains

**Setup:**
```bash
cd Agents
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
jupyter notebook
```

**Key Technologies:**
- LangChain 1.2.0
- Pydantic 2.12.5
- Euron AI
- Python 3.10

### 2. **MediChatbot** (`MediChatbot/`)
Medical chatbot with RAG (Retrieval Augmented Generation) capabilities.

**Features:**
- PDF processing for medical documents
- Vector store integration
- Context-aware responses
- Email utilities for notifications

### 3. **FastAPI Projects** (`FASTAPI/`, `FASTAPI_WITH_DATABASE/`)
RESTful API implementations with FastAPI.

**Features:**
- Database integration
- Authentication
- CRUD operations
- API documentation with Swagger

### 4. **Data Preprocessing** (`Data_Preprocessing/`)
Text preprocessing pipelines for NLP tasks.

**Includes:**
- IMDB dataset processing
- Text cleaning and normalization
- Tokenization examples

## 🛠️ Technologies Used

- **AI/ML Frameworks:**
  - LangChain 1.x
  - LangGraph
  - Euron AI
  - OpenAI API

- **Backend:**
  - FastAPI
  - Python 3.10+
  - MongoDB

- **Vector Databases:**
  - Custom vector store implementations
  - Embeddings management

- **Development Tools:**
  - Jupyter Notebooks
  - Git
  - Virtual Environments

## 📋 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git
- Jupyter Notebook (for notebook examples)

## 🚀 Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/Aman-Husain-123/GenerativeAI_Learning_Journey.git
cd GenerativeAI_Learning_Journey
```

2. **Choose a project and navigate to its directory:**
```bash
cd Agents  # or any other project
```

3. **Create and activate virtual environment:**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

6. **Run the project:**
```bash
jupyter notebook  # For notebook projects
# or
python main.py  # For Python scripts
```

## 🔑 Environment Variables

Most projects require API keys. Create a `.env` file in the project directory:

```env
# Euron AI (for Agents project)
EURON_API_KEY=your_api_key_here

# OpenAI (if applicable)
OPENAI_API_KEY=your_openai_key_here

# MongoDB (if applicable)
MONGODB_URI=your_mongodb_uri_here
```

**⚠️ Never commit `.env` files to version control!**

## 📖 Learning Path

### Beginner
1. Start with `Data_Preprocessing/` to understand text processing
2. Explore `API_Example/` for basic API interactions
3. Try `Example2/` for simple implementations

### Intermediate
1. Dive into `Langchain/` for LangChain basics
2. Explore `FASTAPI/` for API development
3. Work with `Mongo_DB/` for database integration

### Advanced
1. Build agents in `Agents/` with LangChain 1.x
2. Implement RAG systems in `MediChatbot/`
3. Deploy models with `Model_Serving_On_Cloud/`

## 🤝 Contributing

This is a personal learning repository, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Notes

- Each project has its own README with specific instructions
- Virtual environments are excluded from git (`.gitignore`)
- API keys and sensitive data are never committed
- Some projects require specific Python versions (check individual READMEs)

## 🐛 Known Issues

### Agents Project
- **Issue:** Pydantic compatibility with `euriai` package
- **Solution:** Use Python 3.10 with Pydantic 2.12.5
- **Kernel:** Select "Python 3.10 (Agents)" kernel in Jupyter

### LangChain Projects
- **Issue:** LangChain 1.x breaking changes
- **Solution:** Use `InMemoryChatMessageHistory` instead of old memory classes
- **Note:** `create_react_agent` moved to `langgraph.prebuilt`

## 📚 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Euron AI Documentation](https://euron.one/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 📧 Contact

**Aman Husain**
- GitHub: [@Aman-Husain-123](https://github.com/Aman-Husain-123)
- Repository: [GenerativeAI_Learning_Journey](https://github.com/Aman-Husain-123/GenerativeAI_Learning_Journey)

## 📄 License

This project is for educational purposes. Individual components may have their own licenses.

## 🙏 Acknowledgments

- LangChain community for excellent documentation
- Euron AI for API access
- All open-source contributors whose tools made this possible

---

⭐ **Star this repository if you find it helpful!**

🔔 **Watch for updates as I continue my AI learning journey!**

📖 **Check individual project READMEs for detailed instructions**
