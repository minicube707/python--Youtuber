from mcp.server.mcpserver import MCPServer


# Create the MCP server instance
app = MCPServer()


# Register a tool that returns the user's favorite color
@app.tool()
def get_favorite_color() -> str:
    return 'Teal'


if __name__ == '__main__':
    # Start the MCP server using Streamable HTTP transport
    app.run(transport='streamable-http')
