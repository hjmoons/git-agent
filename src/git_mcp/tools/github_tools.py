from fastmcp import FastMCP
from github import Github, GithubException, UnknownObjectException, RateLimitExceededException
from typing import List, Dict, Callable
import os

# MCP 인스턴스를 변수로 받아 GitHub 도구 등록
def register_github_tools(mcp: FastMCP) -> None:
    # 1. git 최근 commit 내역 불러오기
    @mcp.tool()
    def get_recent_github_commits(owner: str, repo_path: str, branch: str=None, count: int=5) -> List[Dict]:
        try:
            token = os.getenv("GITHUB_TOKEN")
            github = Github(token) if token else Github()
            repo = github.get_repo(f"{owner}/{repo_path}")

            commits_data = []

            if branch:
                for commit in repo.get_commits(sha=branch)[:count]:
                    commits_data.append({
                        "sha": commit.sha[:7],
                        "author": commit.commit.author.name,
                        "date": commit.commit.author.date.isoformat(),
                        "message": commit.commit.message.split("\n")[0]
                    })
            else:
                for commit in repo.get_commits()[:count]:
                    commits_data.append({
                        "sha": commit.sha[:7],
                        "author": commit.commit.author.name,
                        "date": commit.commit.author.date.isoformat(),
                        "message": commit.commit.message.split("\n")[0]
                    })
            
            return commits_data
        except UnknownObjectException:
            raise Exception(f"Repository '{owner}/{repo_path}' not found or private")
        except GithubException as e:
            if e.status == 404 and branch:
                raise Exception(f"Branch '{branch}' not found in {owner}/{repo_path}")
            elif e.status == 409:
                raise Exception(f"Repository is empty")
            else:
                raise Exception(f"GitHub API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to get commits: {str(e)}")