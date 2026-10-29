"""Lab: Skill 1.5.6, part 3 - an MCP client that discovers the search tool and lets a Bedrock model use it.

  python mcp_client.py                 # list the server's tools and call one directly
  python mcp_client.py --with-model    # hand the MCP tools to Nova 2 Lite through the Converse API
"""
import asyncio, json, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from tool_calling import run_with_tools

SERVER = StdioServerParameters(command=sys.executable, args=["mcp_server.py"])


async def main(with_model):
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            for t in tools:
                print(f"tool: {t.name}\n  {t.description}\n  schema: {json.dumps(t.inputSchema)}")

            if not with_model:
                res = await session.call_tool("search_knowledge", {"query": "BP-18-4Ah charge time", "k": 2})
                print("\ndirect call:\n" + res.content[0].text)
                return

            # Bedrock tool specs built from whatever the MCP server advertises: no hard-coded schema.
            specs = [{"toolSpec": {"name": t.name, "description": t.description or t.name,
                                   "inputSchema": {"json": t.inputSchema}}} for t in tools]
            loop = asyncio.get_running_loop()

            def call_tool(name, args):
                fut = asyncio.run_coroutine_threadsafe(session.call_tool(name, args), loop)
                return json.loads(fut.result().content[0].text)

            q = "My order includes a BP-18-4Ah battery. How long does it take to charge, and is it under warranty?"
            print(f"\nQ: {q}")
            answer = await loop.run_in_executor(None, run_with_tools, q, specs, call_tool)
            print("A: " + answer)


if __name__ == "__main__":
    asyncio.run(main("--with-model" in sys.argv))
