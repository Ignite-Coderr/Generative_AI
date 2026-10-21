from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

# Vector DB imports
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter


# ============================
# 1. Graph State
# ============================

class GraphState(TypedDict):
    query: str
    intent: Optional[str]
    retrieved_docs: Optional[str]
    answer: Optional[str]


# ============================
# 2. RAG Setup (Local)
# ============================

loader = TextLoader("rag_data.txt")
documents = loader.load()

splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
docs = splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()


# ============================
# 3. Nodes
# ============================

# ---- Intent Classifier (Local Logic)
def classify_intent(state: GraphState):
    query = state["query"].lower()

    if any(char.isdigit() for char in query):
        intent = "math"
    elif "langgraph" in query or "framework" in query or "document" in query:
        intent = "rag"
    else:
        intent = "general"

    print(f"[Classifier] Intent: {intent}")
    return {"intent": intent}


# ---- General Response Node
def general_node(state: GraphState):
    response = f"General response: You asked '{state['query']}'"
    return {"answer": response}


# ---- Retriever Node
def retrieve_node(state: GraphState):
    docs = retriever.invoke(state["query"])
    context = "\n".join([d.page_content for d in docs])

    print("[Retriever] Documents fetched")
    return {"retrieved_docs": context}


# ---- RAG Node
def rag_node(state: GraphState):
    answer = f"""
Context-based answer:

{state['retrieved_docs']}

Question: {state['query']}
"""
    return {"answer": answer}


# ---- Calculator Node
def math_node(state: GraphState):
    try:
        result = eval(state["query"])
        return {"answer": f"Math result: {result}"}
    except:
        return {"answer": "Invalid math expression"}


# ============================
# 4. Graph Construction
# ============================

builder = StateGraph(GraphState)

# Add nodes
builder.add_node("classifier", classify_intent)
builder.add_node("general", general_node)
builder.add_node("retrieve", retrieve_node)
builder.add_node("rag", rag_node)
builder.add_node("math", math_node)

# Entry point
builder.set_entry_point("classifier")


# ---- Routing Logic
def route_intent(state: GraphState):
    return state["intent"]


builder.add_conditional_edges(
    "classifier",
    route_intent,
    {
        "general": "general",
        "rag": "retrieve",
        "math": "math",
    },
)

# RAG flow
builder.add_edge("retrieve", "rag")

# End edges
builder.add_edge("general", END)
builder.add_edge("rag", END)
builder.add_edge("math", END)

# Compile graph
graph = builder.compile()


# ============================
# 5. Run Loop
# ============================

if __name__ == "__main__":
    print("Local LangGraph Router (No API Key Needed)")
    print("Type 'exit' to quit\n")

    while True:
        query = input("Ask: ")

        if query.lower() == "exit":
            break

        result = graph.invoke({
            "query": query,
            "intent": None,
            "retrieved_docs": None,
            "answer": None
        })

        print("\nFinal Answer:")
        print(result["answer"])
        print("-" * 50)
