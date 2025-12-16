from fastmcp import FastMCP
from tools import register_git_tools

mcp = FastMCP("Git-Agent")
register_git_tools(mcp)

if __name__ == "__main__":
    mcp.run()
    