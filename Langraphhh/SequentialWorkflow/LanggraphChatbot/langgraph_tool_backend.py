# backend.py

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from dotenv import load_dotenv
import sqlite3
import requests

load_dotenv()

# -------------------
# 1. LLM
# -------------------
llm = ChatOpenAI()

# -------------------
# 2. Tools
# -------------------
# Tools
search_tool = DuckDuckGoSearchRun(region="us-en")

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}

@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    r = requests.get(url)
    return r.json()



@tool
def check_train_availability(origin: str, destination: str, date: str) -> dict:
    """
    Check train availability between an origin and destination station for a given date.
    Args:
        origin: Departure station or city (e.g. 'Delhi', 'Mumbai')
        destination: Arrival station or city (e.g. 'Mumbai', 'Bangalore')
        date: Travel date in YYYY-MM-DD or readable format (e.g. '2026-09-25')
    """
    return {
        "origin": origin,
        "destination": destination,
        "date": date,
        "available_trains": [
            {
                "train_name": f"{origin.title()}-{destination.title()} Superfast Express",
                "train_number": "12952",
                "departure_time": "08:00 AM",
                "arrival_time": "04:30 PM",
                "status": "Available (34 seats left)",
                "class": "3A / 2A / 1A",
                "fare": "₹1,450"
            },
            {
                "train_name": "Rajdhani Express",
                "train_number": "12431",
                "departure_time": "04:15 PM",
                "arrival_time": "11:00 PM",
                "status": "Available (12 seats left)",
                "class": "2A / 1A",
                "fare": "₹2,200"
            }
        ]
    }

@tool
def check_flight_availability(origin: str, destination: str, date: str) -> dict:
    """
    Check flight availability between an origin and destination airport/city for a given date.
    Args:
        origin: Departure city or airport code (e.g. 'DEL', 'Delhi')
        destination: Arrival city or airport code (e.g. 'BOM', 'Mumbai')
        date: Travel date in YYYY-MM-DD or readable format (e.g. '2026-09-25')
    """
    return {
        "origin": origin,
        "destination": destination,
        "date": date,
        "available_flights": [
            {
                "airline": "IndiGo",
                "flight_number": "6E-204",
                "departure_time": "06:15 AM",
                "arrival_time": "08:25 AM",
                "duration": "2h 10m",
                "status": "Available",
                "price": "₹4,850"
            },
            {
                "airline": "Air India",
                "flight_number": "AI-502",
                "departure_time": "01:30 PM",
                "arrival_time": "03:45 PM",
                "duration": "2h 15m",
                "status": "Available",
                "price": "₹5,400"
            }
        ]
    }

tools = [search_tool, get_stock_price, calculator, check_train_availability, check_flight_availability]
llm_with_tools = llm.bind_tools(tools)

# -------------------
# 3. State
# -------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# -------------------
# 4. Nodes
# -------------------
def chat_node(state: ChatState):
    """LLM node that may answer or request a tool call."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

# -------------------
# 5. Checkpointer
# -------------------
conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

# -------------------
# 6. Graph
# -------------------
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")

graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge('tools', 'chat_node')

chatbot = graph.compile(checkpointer=checkpointer)

# -------------------
# 7. Helper
# -------------------
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)    