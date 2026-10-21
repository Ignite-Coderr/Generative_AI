from mem0 import Memory
from openai import OpenAI

OPENAI_API_KEY = "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"

QUADRANT_HOST = "localhost"

NEO4J_URL="bolt://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="reform-william-center-vibrate-press-5829"


# What does it doing here is that we are creating a configuration dictionary that specifies the providers and their configurations for the embedder, LLM, vector store, and graph store. This configuration is then used to initialize a Memory client, which can be used to perform operations like searching and adding memories. The chat function demonstrates how to use the Memory client to search for relevant memories based on a user query, generate a response using the LLM, and then add the conversation to the memory store.
config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {"api_key": OPENAI_API_KEY, "model": "text-embedding-3-small"},
    },
    "llm": {"provider": "openai", "config": {"api_key": OPENAI_API_KEY, "model": "gpt-4.1"}},
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": QUADRANT_HOST,
            "port": 6333,
        },
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {"url": NEO4J_URL, "username": NEO4J_USERNAME, "password": NEO4J_PASSWORD},
    },
}

# Initialize Memory client and OpenAI client for LLM interactions
mem_client = Memory.from_config(config)
openai_client = OpenAI(api_key=OPENAI_API_KEY)


# Example chat function that demonstrates how to use the Memory client to search for relevant memories, generate a response using the LLM, and add the conversation to the memory store.
def chat(message):
    # Search for relevant memories based on the user query. The search function will return a list of memories that are relevant to the input message, which can then be used to provide context for generating a response. The user_id is specified to associate the search with a particular user, allowing for personalized interactions in future queries.
    mem_result = mem_client.search(query=message, user_id="p123")

    print("mem_result", )

    # Extract the memory content from the search results and concatenate them into a single string. This will be used to provide context for the LLM when generating a response. Each memory is separated by a newline for better readability.
    memories = "\n".join([m["memory"] for m in mem_result.get("results")])

    print(f"\n\nMEMORY:\n\n{memories}\n\n")
    
    # Define a system prompt that instructs the LLM on how to use the retrieved memories to generate a response. The prompt emphasizes the role of the LLM as a Memory-Aware Fact Extraction Agent, guiding it to analyze the input content, extract structured knowledge, and maintain an optimized memory store. The tone is set to be professional and analytical, with a focus on precision and clear signaling of uncertainty when necessary. The retrieved memories are included in the prompt to provide context for the LLM's response generation.
    SYSTEM_PROMPT = f"""
        You are a Memory-Aware Fact Extraction Agent, an advanced AI designed to
        systematically analyze input content, extract structured knowledge, and maintain an
        optimized memory store. Your primary function is information distillation
        and knowledge preservation with contextual awareness.

        Tone: Professional analytical, precision-focused, with clear uncertainty signaling
        
        Memory and Score:
        {memories}
    """
    messages = [
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": message }
    ]

    # Generate a response using the LLM based on the user query and the retrieved memories. The LLM will analyze the input, extract relevant information, and provide a response that is informed by the context of the retrieved memories. The response will also include any new information that can be added to the memory store for future reference.
    result = openai_client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    )

    # Add the user query and the assistant's response to the memory store so that it can be referenced in future interactions. This allows the system to build a more comprehensive memory over time, improving its ability to provide informed responses based on past interactions and retrieved memories.
    messages.append(
        { "role": "assistant", "content": result.choices[0].message.content }
    )

    # Here we are adding the conversation (both the user query and the assistant's response) to the memory store using the Memory client. This allows the system to retain this information for future interactions, enabling it to provide more informed responses based on past conversations and retrieved memories. The user_id is specified to associate this memory with a particular user, allowing for personalized interactions in future queries.
    mem_client.add(messages, user_id="p123")

    return result.choices[0].message.content

while True:
    message = input(">> ")
    print("BOT: ", chat(message=message))
    



# TODO: Write the entire flow of the code step by step:
# 1. We define a configuration dictionary that specifies the providers and their configurations for the embedder, LLM, vector store, and graph store.
# 2. We initialize a Memory client using the configuration dictionary. This client will be used to perform operations like searching and adding memories.
# 3. We also initialize an OpenAI client for interacting with the LLM.
# 4. We define a chat function that takes a user message as input.
# 5. Inside the chat function, we first search for relevant memories based on the user
    # query using the Memory client's search function. The search results are associated with a specific user_id for personalized interactions.
# 6. We extract the memory content from the search results and concatenate them into a single string to provide context for the LLM.
# 7. We define a system prompt that instructs the LLM on how to use the retrieved memories to generate a response. The prompt emphasizes the role of the LLM as a Memory-Aware Fact Extraction Agent, guiding it to analyze the input content, extract structured knowledge, and maintain an optimized memory store.
# 8. We create a list of messages that includes the system prompt and the user message.
# 9. We generate a response using the OpenAI client by calling the chat completions API with the defined messages and the specified model.
# 10. We add the user query and the assistant's response to the memory store using the Memory client's add function, associating it with the same user_id for future reference.
# 11. Finally, we return the assistant's response to the user.  


# TODO: Data flow in general term like where data is coming from and where it is going to:
# 1. The user inputs a message through the chat interface.
# 2. The message is passed to the chat function, which processes it to generate a response.
# 3. The chat function first searches for relevant memories in the Memory client based on the user message, retrieving any past interactions or information that may be relevant to the current query.
# 4. The retrieved memories are then used to construct a system prompt that provides context for the LLM.
# 5. The system prompt and the user message are sent to the OpenAI client to generate a response using the specified LLM model.
# 6. The generated response is then added to the Memory client along with the user message, allowing the system to retain this information for future interactions.
# 7. Finally, the generated response is returned to the user, completing the interaction cycle. The system can then use the stored memories in future interactions to provide more informed and contextually relevant responses based on past conversations.


# Now build a project where i am giving docs and it is been transfomrmed into knowledge graph and then i can query the knowledge graph and get the answer.
# Give code for the entire project step by step.
import os
from mem import chat
from openai import OpenAI

OPENAI_API_KEY = "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" 



