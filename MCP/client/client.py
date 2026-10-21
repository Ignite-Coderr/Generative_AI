import asyncio
import os

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent

# Load environment variables (OPENAI_API_KEY, etc.)
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not set in environment or .env")

# TODO:Create server parameters for stdio connection
# Use module form so Python finds server/server.py reliably
server_params = StdioServerParameters(
    command="python",
    args=["-m", "server.server"],
)


async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection (handshake with server)
            await session.initialize()

            # Load MCP tools from the server
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_agent("openai:gpt-4.1", tools)
            agent_response = await agent.ainvoke(
                {"messages": "What is (4 + 5)?"}
            )

            # Return the full response so __main__ can inspect/print it
            return agent_response


if __name__ == "__main__":
    result = asyncio.run(run_agent())
    # For debugging, just print the whole result structure
    print(result)
    # If you know the structure and want only the model's reply, you can later do e.g.: