from fastmcp import FastMCP
from git import Repo, InvalidGitRepositoryError, GitCommandError
from typing import List, Dict, Callable

# MCP 인스턴스를 변수로 받아 Git 도구 등록
def register_git_tools(mcp_instance: FastMCP) -> None:
    # 1. git 최근 commit 내역 불러오기
    @mcp_instance.tool()
    def get_recent_commits(repo_path: str, count: int=5) -> List[Dict]:
        try:
            repo = Repo(repo_path)
            commits_data = []

            for commit in repo.iter_commits(max_count=count):
                commits_data.append({
                    "sha": commit.hexsha,
                    "author": commit.author.name,
                    "date": commit.authored_datetime.isoformat(),
                    "message": commit.message.strip()
                })
            
            return commits_data
        except InvalidGitRepositoryError:
            return {"error": f"Invalid Git Repository path: {repo_path}"}
        except Exception as e:
            return {"error": str(e)}