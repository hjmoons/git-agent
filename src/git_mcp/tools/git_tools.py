from fastmcp import FastMCP
from git import Repo, InvalidGitRepositoryError, GitCommandError
from typing import List, Dict, Callable

# MCP 인스턴스를 변수로 받아 Git 도구 등록
def register_git_tools(mcp: FastMCP) -> None:
    # 1. git 최근 commit 내역 불러오기
    @mcp.tool()
    def get_recent_git_commits(repo_path: str, branch: str=None, count: int=5) -> List[Dict]:
        try:
            repo = Repo(repo_path)
            commits_data = []

            if branch:
                for commit in repo.iter_commits(branch, max_count=count):
                    commits_data.append({
                        "sha": commit.hexsha,
                        "author": commit.author.name,
                        "date": commit.authored_datetime.isoformat(),
                        "message": commit.message.strip(),
                    })
            else:
                for commit in repo.iter_commits(max_count=count, all=True):
                    commits_data.append({
                        "sha": commit.hexsha,
                        "author": commit.author.name,
                        "date": commit.authored_datetime.isoformat(),
                        "message": commit.message.strip(),
                    })
            
            return commits_data
        except InvalidGitRepositoryError:
            raise Exception(f"Invalid Git Repository path: {repo_path}")
        except GitCommandError as e:
            if branch:
                branch_names = [b.name for b in Repo(repo_path).branches]
                raise Exception(f"Branch '{branch}' not found. Available branched: {', '.join(branch_names)}")
            raise Exception(f"Git command error: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to get commits: {str(e)}")