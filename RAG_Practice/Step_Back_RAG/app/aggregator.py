from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def update_context(existing_context, new_docs):
    docs_text = "\n\n".join(new_docs)

    prompt = f"""
Existing Context:
{existing_context}

New Information:
{docs_text}

Merge and refine into a concise updated context.
"""
    return llm.invoke(prompt).content
