from fastmcp import Client
import asyncio

async def test_git_tools():
    print("-" * 10)
    print("클라이언트 생성 중")

    client = Client(r".\src\git_mcp\server.py")

    try:
        async with client:
            print("-" * 10)
            print("클라이언트 연결됨")

            commit_result = await client.call_tool("get_recent_commits", {"repo_path": r"C:\Users\mhj59\IdeaProjects\git-agent"})

            # 구조화된 데이터만 출력
            for commit in commit_result.structured_content['result']:
                print(f"[{commit['sha'][:8]}] {commit['message']}")
                print(f"  작성자: {commit['author']}")
                print(f"  날짜: {commit['date']}\n")

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        print("-" * 10)
        print("클라이언트 상호작용 완료")

if __name__ == "__main__":
    asyncio.run(test_git_tools())