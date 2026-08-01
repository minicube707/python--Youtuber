from fastmcp import FastMCP

# Create a new MCP server named "Demo".
# This server will expose tools that can be called by an MCP client.
mcp = FastMCP("Demo")


# Register this function as an MCP tool.
# The language model can call this function when it needs to add two numbers.
@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Register this function as an MCP tool.
# The language model can call this function when it needs to add two numbers.
@mcp.tool
def sub(a: int, b: int) -> int:
    """Sub two numbers"""
    return a - b


# Register this function as another MCP tool.
# The language model can call this function to multiply two numbers.
@mcp.tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

# Register this function as another MCP tool.
# The language model can call this function to multiply two numbers.
@mcp.tool
def divide(a: int, b: int) -> int:
    """Divide two numbers"""
    return a * b


# Start the MCP server when this file is executed directly.
# The server will wait for incoming requests from MCP clients.
if __name__ == "__main__":
    mcp.run()