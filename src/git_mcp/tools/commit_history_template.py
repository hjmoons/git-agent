"""
Commit History Markdown 템플릿 생성
"""
from typing import List, Dict, Any
from datetime import datetime


def generate_commit_history_markdown(commits: List[Dict[str, Any]]) -> str:
    """
    커밋 리스트를 받아서 완전한 Markdown 히스토리 문서를 생성합니다.

    Args:
        commits: 커밋 딕셔너리 리스트 (get_recent_github_commits 반환 형식)
                 각 커밋은 date, sha, author, message, stats 필드를 포함

    Returns:
        완전한 Markdown 히스토리 문서
    """
    rows = []
    for commit in commits:
        date = commit.get("date", "")
        sha = commit.get("sha", "")
        author = commit.get("author", "N/A")
        message = commit.get("message", "N/A")
        stats = commit.get("stats", {})
        file_count = stats.get("total_files", 0)

        # ISO 형식을 YYYY-MM-DD로 변환
        if date:
            try:
                dt = datetime.fromisoformat(date.replace('Z', '+00:00'))
                date_str = dt.strftime("%Y-%m-%d")
            except:
                date_str = date[:10]  # 앞 10자리만
        else:
            date_str = "N/A"

        # 메시지에서 파이프(|) 문자 이스케이프
        message = message.replace("|", "\\|") if message else "N/A"

        # Markdown 테이블 행 생성
        row = f"| {date_str} | {sha} | {author} | {message} | {file_count} |"
        rows.append(row)

    # 헤더 + 모든 행
    header = "# Commit 내역\n\n"
    header += "| 날짜 | SHA | 생성자 | 내용요약 | 파일개수 |\n"
    header += "| --- | --- | --- | --- | --- |\n"

    return header + "\n".join(rows) + "\n"


def append_commits_to_history(existing_content: str, commits: List[Dict[str, Any]]) -> str:
    """
    기존 history.md에 새로운 커밋들을 추가합니다.

    Args:
        existing_content: 기존 파일 내용
        commits: 추가할 커밋 리스트

    Returns:
        업데이트된 Markdown 내용
    """
    # 기존 파일이 비어있거나 헤더가 없으면 새로 생성
    if not existing_content or "# Commit 내역" not in existing_content:
        return generate_commit_history_markdown(commits)

    # 새로운 행들 생성
    rows = []
    for commit in commits:
        date = commit.get("date", "")
        sha = commit.get("sha", "")
        author = commit.get("author", "N/A")
        message = commit.get("message", "N/A")
        stats = commit.get("stats", {})
        file_count = stats.get("total_files", 0)

        # ISO 형식을 YYYY-MM-DD로 변환
        if date:
            try:
                dt = datetime.fromisoformat(date.replace('Z', '+00:00'))
                date_str = dt.strftime("%Y-%m-%d")
            except:
                date_str = date[:10]
        else:
            date_str = "N/A"

        message = message.replace("|", "\\|") if message else "N/A"
        row = f"| {date_str} | {sha} | {author} | {message} | {file_count} |"
        rows.append(row)

    # 기존 내용 끝에 새로운 행 추가
    result = existing_content.rstrip() + "\n"
    result += "\n".join(rows) + "\n"

    return result
