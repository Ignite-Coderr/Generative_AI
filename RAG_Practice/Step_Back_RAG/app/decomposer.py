from langchain.chat_models import ChatOpenAI
from app.config import *

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def decompose_query(question):
    prompt = f"""
Break the question into {SUB_QUERY_COUNT} smaller search queries.

Question: {question}
Return each query on a new line.
"""
    response = llm.invoke(prompt).content
    queries = [q.strip() for q in response.split("\n") if q.strip()]
    return queries[:SUB_QUERY_COUNT]
