from fastmcp import FastMCP
from github import Github, GithubException, UnknownObjectException, RateLimitExceededException
from typing import List, Dict, Callable
import os
from .commit_history_template import generate_commit_history_markdown, append_commits_to_history

# MCP 인스턴스를 변수로 받아 GitHub 도구 등록
def register_github_tools(mcp: FastMCP) -> None:
    # 1. git 최근 commit 내역 불러오기
    @mcp.tool()
    def get_recent_github_commits(owner: str, repo_path: str, branch: str="main", count: int=5) -> List[Dict]:
        try:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                raise Exception("GITHUB_TOKEN environment variable is required")
            
            github = Github(token, verify=False) if token else Github()
            repo = github.get_repo(f"{owner}/{repo_path}")

            commits_data = []

            for commit in repo.get_commits(sha=branch)[:count]:
                diff_list = []
                files = sorted(list(commit.files), key=lambda f: f.additions + f.deletions, reverse=True)[:10]

                for file in files:
                    diff_list.append({
                        "name": file.filename,
                        "status": file.status,
                        "add": file.additions,
                        "del": file.deletions,
                        "patch": file.patch[:2000] if file.patch else None,
                        "url": file.blob_url
                    })

                commits_data.append({
                    "sha": commit.sha[:7],
                    "author": commit.commit.author.name,
                    "date": commit.commit.author.date.isoformat(),
                    "message": commit.commit.message.split("\n")[0],
                    "stats": {
                        "total_files": len(files),
                        "additions": commit.stats.additions,
                        "deletions": commit.stats.deletions
                    },
                    "files": diff_list
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

    # 2. 요약된 커밋 내역을 Markdown으로 만들어서 GitHub에 커밋
    @mcp.tool()
    def commit_history_to_github(owner: str, repo_path: str, commits: List[Dict], branch: str = "main", history_file: str = "history.md") -> Dict:
        try:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                raise Exception("GITHUB_TOKEN environment variable is required")

            # 1. Markdown 문서 생성
            markdown_content = generate_commit_history_markdown(commits)

            # 2. GitHub API로 파일 커밋
            github = Github(token, verify=False) if token else Github()
            repo = github.get_repo(f"{owner}/{repo_path}")

            commit_message = f"docs: Update commit history - {len(commits)} commits analyzed"

            # 기존 파일이 있는지 확인
            try:
                file = repo.get_contents(history_file, ref=branch)
                sha = file.sha
                # 파일 업데이트
                result = repo.update_file(
                    path=history_file,
                    message=commit_message,
                    content=markdown_content,
                    sha=sha,
                    branch=branch
                )
            except UnknownObjectException:
                # 파일이 없으면 새로 생성
                result = repo.create_file(
                    path=history_file,
                    message=commit_message,
                    content=markdown_content,
                    branch=branch
                )

            return {
                "success": True,
                "commits_processed": len(commits),
                "file_path": history_file,
                "commit_sha": result["commit"].sha[:7],
                "commit_url": result["commit"].html_url,
                "file_url": result["content"].html_url
            }

        except UnknownObjectException:
            raise Exception(f"Repository '{owner}/{repo_path}' not found or private")
        except GithubException as e:
            if e.status == 403:
                raise Exception(f"Permission denied. Check GITHUB_TOKEN permissions.")
            elif e.status == 404:
                raise Exception(f"Branch '{branch}' not found in {owner}/{repo_path}")
            else:
                raise Exception(f"GitHub API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to commit history to GitHub: {str(e)}")