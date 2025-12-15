from fastmcp import FastMCP
from tools import register_git_tools

def main():
    mcp = FastMCP("Git-Agent")
    register_git_tools(mcp)
    mcp.run(transport="http", host="127.0.0.1", port=8080)

if __name__ == "__main__":
    main() 
    