# math_server.py
from mcp.server.fastmcp import FastMCP

# TODO: It is for demonstration purposes. You can replace it with your own tools and logic.
mcp = FastMCP("Math")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def get_whether(city: str) -> str:
    """Get whether of a city"""
    return f"The whether of {city} is sunny."

if __name__ == "__main__":
    mcp.run(transport="stdio")