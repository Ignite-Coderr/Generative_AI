from dotenv import load_dotenv
load_dotenv()

from .graph import create_chat_graph
import json
from langgraph.types import Command
from langgraph.checkpoint.mongodb import MongoDBSaver
MONGODB_URI = "mongodb://admin:admin@localhost:27018"
config = {"configurable": {"thread_id": "7"}}
 
def init():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph_with_mongo = create_chat_graph(checkpointer=checkpointer)
    
        state = graph_with_mongo.get_state(config=config)
        
        # If there is no existing state (new thread), start a new conversation
        if not state.values or "messages" not in state.values:
            print("No existing state found. Initiating a new conversation to trigger the tool...")
            initial_input = {"messages": [{"role": "user", "content": "I need human assistance to process this request."}]}
            for event in graph_with_mongo.stream(initial_input, config, stream_mode="values"):
                if "messages" in event:
                    event["messages"][-1].pretty_print()
            
            # Re-fetch state after the interrupt is hit
            state = graph_with_mongo.get_state(config=config)
        
        last_message = state.values.get('messages', [])[-1] if state.values.get('messages') else None
        
        tool_calls = getattr(last_message, 'tool_calls', []) if last_message else []
        user_query = None

        for call in tool_calls:
            if call.get("name") == "human_assistance_tool":
                user_query = call.get("args", {}).get("query")
        
        if user_query:
            print("User is Tying to Ask:", user_query)
            ans = input("Resolution > ")

            resume_command = Command(resume={"data": ans})
            
            for event in graph_with_mongo.stream(resume_command, config, stream_mode="updates"):
                for node_name, node_state in event.items():
                    if "messages" in node_state:
                         node_state["messages"][-1].pretty_print()
        else:
            print("No active tool interrupt found. Continuing graph execution...")
            for event in graph_with_mongo.stream(None, config, stream_mode="updates"):
                for node_name, node_state in event.items():
                    if "messages" in node_state:
                         node_state["messages"][-1].pretty_print()

init()