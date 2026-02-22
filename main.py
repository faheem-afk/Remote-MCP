import json
from fastmcp import FastMCP


mcp = FastMCP("simple server")

@mcp.tool
def add(a:int, b:int) -> int:
   '''add two numbers together.
   args:
   a: first number
   b: second number
   returns:
   the sum of a and b
   '''
   return a+b

@mcp.resource("info://server")
def server_info()->str:
   '''get information about the server.'''
   info = {
      "name":"simple server",
      "version":"1.0.0",
      "description":"a basic MCP server with math tools",
      "tools": ["add"],
      "author":"Faheem"
   }
   return json.dumps(info, indent=2)

if __name__ == "__main__":
   mcp.run(transport="http", host="0.0.0.0", port=8000)

