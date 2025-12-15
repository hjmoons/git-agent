from fastmcp import FastMCP
from git_mcp.tools import register_git_tools

def test_main():
    """서버 설정과 동일하게 도구 등록 후 테스트"""
    print("=" * 10)
    print("Git Agent MCP 서버 기능 테스트")
    print("=" * 10)

    print("\n[1] MCP 서버 생성 및 도구 등록...")
    mcp = FastMCP("Git-Tool-Test")
    register_git_tools(mcp)
    print("✓ 완료\n")

    # 등록된 도구 목록 확인
    print("[2] 등록된 도구:")
    if hasattr(mcp, '_tools'):
        for tool_name in mcp._tools:
            print(f"  - {tool_name}")
    print()

if __name__ == "__main__":
    test_main()