from app.decomposer import decompose_query
from app.retriever import retrieve
from app.aggregator import update_context
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def run_rag(question):
    sub_queries = decompose_query(question)

    context = ""

    for q in sub_queries:
        docs = retrieve(q)
        context = update_context(context, docs)

    final_prompt = f"""
Context:
{context}

Answer the question:
{question}
"""
    answer = llm.invoke(final_prompt).content

    return answer, sub_queries
