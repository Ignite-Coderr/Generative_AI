import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    QD_HOST = os.getenv("QD_HOST", "localhost")
    QD_PORT = int(os.getenv("QD_PORT", 6333))
    
    # Embedding Configuration
    EMBEDDING_MODEL = "text-embedding-3-small"
    
    # LLM Configuration
    LLM_MODEL = "gpt-4o-mini" # or gpt-4.1-mini as requested
    
    # Chunking Configuration
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100
    
    # Collections
    COLLECTIONS = {
        "html": "html_docs",
        "git": "git_docs",
        "cpp": "cpp_docs",
        "django": "django_docs",
        "sql": "sql_docs",
        "devops": "devops_docs"
    }
    
    # Section Descriptions for Routing
    SECTION_DESCRIPTIONS = {
        "html": "Web structure, tags, elements, attributes, semantic html",
        "git": "Version control, commits, branches, merging, cloning, repositories",
        "sql": "Databases, queries, tables, joins, select, insert, update, delete",
        "django": "Python web framework, models, views, templates, urls, mvt architecture",
        "devops": "Deployment, CI/CD, Docker, Kubernetes, containerization, pipelines",
        "cpp": "Programming, pointers, memory management, classes, object-oriented programming, stl"
    }
