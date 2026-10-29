"""Lab: Skill 1.5.6, part 2 - the same retrieval exposed as an MCP server (stdio transport).

Any MCP client (Claude Desktop, an IDE, Amazon Q Developer, your own agent) can now search the knowledge.
Run directly to test:  python mcp_server.py   (it waits for a client on stdin/stdout)
"""
from mcp.server.fastmcp import FastMCP
import retrieval_api as api

mcp = FastMCP("acme-knowledge")


@mcp.tool(name=api.TOOL_NAME, description=api.TOOL_DESCRIPTION)
def search_knowledge(query: str, k: int = 3) -> dict:
    return api.retrieve(query, k)


if __name__ == "__main__":
    mcp.run()          # stdio by default
