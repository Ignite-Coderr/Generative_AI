import os
import streamlit as st
from dotenv import load_dotenv
from typing_extensions import TypedDict, Annotated

from pyngrok import ngrok
public_url = ngrok.connect(8501).public_url
print(f"Streamlit app is publicly accessible at: {public_url}")

# LangChain / LangGraph
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# ---------------------- ENV ----------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

assert OPENAI_API_KEY, "OPENAI_API_KEY is missing"
assert TAVILY_API_KEY, "TAVILY_API_KEY is missing"

# ---------------------- STREAMLIT CONFIG ----------------------
st.title("Educosys Chatbot App")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(id(st.session_state))

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------- LLM ----------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=OPENAI_API_KEY,
)

# ---------------------- STATE ----------------------
class State(TypedDict):
    messages: Annotated[list, add_messages]

# ---------------------- GRAPH ----------------------
graph_builder = StateGraph(State)

# Tavily Tool (reads TAVILY_API_KEY from env under the hood)
tool = TavilySearchResults(max_results=2)
tools = [tool]

# Bind tools
llm_with_tools = llm.bind_tools(tools)

# Chatbot node
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

# Tool node
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

# Conditional routing
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

# Return to chatbot after tool execution
graph_builder.add_edge("tools", "chatbot")

# Start edge
graph_builder.add_edge(START, "chatbot")

# Memory (LangGraph Checkpointer)
memory = MemorySaver()

# Compile graph
app = graph_builder.compile(checkpointer=memory)

# ---------------------- DISPLAY HISTORY ----------------------
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# ---------------------- USER INPUT ----------------------
if prompt := st.chat_input("Ask anything (web search enabled)..."):
    # Add user message as object (NOT dict)
    user_msg = HumanMessage(content=prompt)
    st.session_state.messages.append(user_msg)

    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call LangGraph with thread_id
    with st.spinner("Thinking..."):
        result = app.invoke(
            {"messages": st.session_state.messages},
            config={
                "configurable": {
                    "thread_id": st.session_state.thread_id
                }
            },
        )

    # Update session messages
    st.session_state.messages = result["messages"]

    # Show latest assistant reply
    last_msg = st.session_state.messages[-1]
    if isinstance(last_msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(last_msg.content)
