from mem0 import Memory
from openai import OpenAI
import os
from dotenv import load_dotenv
# Load .env from the current folder
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
NEO4J_URL = os.getenv("NEO4J_URL", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("reform-william-center-vibrate-press-5829")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in .env")

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {"api_key": OPENAI_API_KEY, "model": "text-embedding-3-small"},
    },
    "llm": {
        "provider": "openai",
        "config": {"api_key": OPENAI_API_KEY, "model": "gpt-4.1"},
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": QDRANT_HOST,   # was QUADRANT_HOST typo
            "port": 6333,
        },
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "bolt://localhost:7687",
            "username": "neo4j",
            "password": "reform-william-center-vibrate-press-5829",
        },
    },
}

# User chat history is stored in memory, which uses the vector store for retrieval and the graph store 
# for reasoning over relationships between memories.
mem_client = Memory.from_config(config)
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def chat(message: str) -> str:
    # Search for relevant memories based on the user message
    mem_result = mem_client.search(query=message, user_id="p123")
    memories = "\n".join(m["memory"] for m in mem_result.get("results", []))

    print(f"\nMEMORY:\n{memories}\n")

    system_prompt = f"""
You are a Memory-Aware Fact Extraction Agent.

Existing memories:
{memories}
"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]

    result = openai_client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
    )

    assistant_msg = result.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_msg})

    mem_client.add(messages, user_id="p123")

    return assistant_msg

if __name__ == "__main__":
    while True:
        user_msg = input(">> ")
        if not user_msg.strip():
            continue
        print("BOT:", chat(user_msg))
