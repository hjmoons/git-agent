"""Entry point for running git_mcp as a module."""
from fastmcp import FastMCP
from git_mcp.tools import register_git_tools, register_github_tools

mcp = FastMCP("Git-Agent")
register_git_tools(mcp)
register_github_tools(mcp)

def main():
    """Run the MCP server"""
    mcp.run()

if __name__ == "__main__":
    main()
