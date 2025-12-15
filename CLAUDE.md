# Git Agent MCP Server

MCP(Model Context Protocol) 서버로, GitHub와 Git 저장소 관리를 위한 다양한 기능을 제공합니다.

## 프로젝트 개요

이 프로젝트는 Claude 및 다른 AI 어시스턴트가 Git 저장소와 상호작용할 수 있도록 하는 MCP 서버입니다. 커밋 내역 조회, PR 관리, 소스코드 비교 등의 기능을 제공합니다.

## 주요 기능

### Git 기능
- **커밋 내역 조회**: 저장소의 커밋 히스토리 확인
- **브랜치 관리**: 브랜치 생성, 삭제, 목록 조회
- **diff/비교**: 커밋 간, 브랜치 간 코드 변경사항 비교
- **로그 분석**: Git 로그 필터링 및 검색
- **상태 확인**: 워킹 디렉토리 및 스테이징 영역 상태

### GitHub 기능
- **Pull Request 관리**
  - PR 목록 조회
  - PR 상세 정보 확인
  - PR 생성 및 수정
  - 리뷰 코멘트 조회
- **Issue 관리**
  - Issue 목록 및 상세 정보
  - Issue 생성 및 수정
- **저장소 정보**
  - 저장소 메타데이터
  - 기여자 정보
  - 릴리스 정보

## 기술 스택

- **언어**: Python 3.10+
- **프로토콜**: MCP (Model Context Protocol)
- **주요 라이브러리**:
  - `mcp` - MCP 서버 SDK
  - `PyGithub` - GitHub REST API 클라이언트
  - `GitPython` - Git 저장소 조작
  - `httpx` - 비동기 HTTP 클라이언트
  - `pydantic` - 데이터 검증 및 타입 힌팅

## 프로젝트 구조

```
git-agent/
├── src/
│   ├── git_agent/
│   │   ├── __init__.py
│   │   ├── server.py          # MCP 서버 진입점
│   │   ├── tools/             # MCP 도구 정의
│   │   │   ├── __init__.py
│   │   │   ├── git_tools.py   # Git 관련 도구
│   │   │   └── github_tools.py # GitHub 관련 도구
│   │   ├── services/          # 비즈니스 로직
│   │   │   ├── __init__.py
│   │   │   ├── git_service.py
│   │   │   └── github_service.py
│   │   └── models/            # Pydantic 모델
│   │       ├── __init__.py
│   │       ├── git_models.py
│   │       └── github_models.py
├── tests/                     # 테스트 코드
│   ├── __init__.py
│   ├── test_git_tools.py
│   └── test_github_tools.py
├── pyproject.toml             # 프로젝트 설정 및 의존성
├── README.md
└── .env.example               # 환경 변수 예시
```

## MCP Tools 설계

### Git Tools

1. **git_log**
   - 커밋 내역 조회
   - 입력: repo_path, limit, branch, author
   - 출력: 커밋 리스트 (hash, author, date, message)

2. **git_diff**
   - 코드 변경사항 비교
   - 입력: repo_path, from, to (commit/branch)
   - 출력: diff 내용

3. **git_status**
   - 워킹 디렉토리 상태
   - 입력: repo_path
   - 출력: modified, staged, untracked 파일 목록

4. **git_show**
   - 특정 커밋 상세 정보
   - 입력: repo_path, commit_hash
   - 출력: 커밋 정보 + diff

5. **git_branch_list**
   - 브랜치 목록
   - 입력: repo_path, remote
   - 출력: 브랜치 리스트

### GitHub Tools

1. **github_list_prs**
   - PR 목록 조회
   - 입력: owner, repo, state, limit
   - 출력: PR 리스트

2. **github_get_pr**
   - PR 상세 정보
   - 입력: owner, repo, pr_number
   - 출력: PR 상세 + 변경 파일 + 리뷰 코멘트

3. **github_compare**
   - 브랜치/커밋 비교
   - 입력: owner, repo, base, head
   - 출력: 변경사항 요약 + 파일 diff

4. **github_list_issues**
   - Issue 목록
   - 입력: owner, repo, state, labels
   - 출력: Issue 리스트

5. **github_get_commits**
   - 커밋 내역 (GitHub API 기반)
   - 입력: owner, repo, branch, limit
   - 출력: 커밋 리스트 + 상세 정보

## 개발 가이드

### 환경 설정

```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화 (Windows)
venv\Scripts\activate

# 가상 환경 활성화 (Linux/Mac)
source venv/bin/activate

# 의존성 설치
pip install -e ".[dev]"

# 또는 uv 사용 (권장)
uv pip install -e ".[dev]"

# 개발 모드 실행
python -m git_agent.server

# 테스트
pytest

# 타입 체크
mypy src/git_agent
```

### 환경 변수

```env
GITHUB_TOKEN=your_github_personal_access_token
DEFAULT_REPO_PATH=/path/to/default/repo
```

### 의존성 (pyproject.toml)

```toml
[project]
name = "git-agent"
version = "0.1.0"
description = "MCP server for Git and GitHub management"
requires-python = ">=3.10"
dependencies = [
    "mcp>=0.1.0",
    "PyGithub>=2.0.0",
    "GitPython>=3.1.0",
    "httpx>=0.25.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "mypy>=1.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]
```

### MCP 서버 연결

Claude Desktop 설정 파일 (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "git-agent": {
      "command": "python",
      "args": ["-m", "git_agent.server"],
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
```

또는 uv 사용:

```json
{
  "mcpServers": {
    "git-agent": {
      "command": "uv",
      "args": ["--directory", "/path/to/git-agent", "run", "git-agent"],
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
```

## 사용 예시

### 커밋 내역 조회
```
User: 최근 10개 커밋을 보여줘
Claude: [git_log 도구 사용하여 커밋 내역 표시]
```

### PR 분석
```
User: #123 PR의 변경사항을 분석해줘
Claude: [github_get_pr 도구로 PR 정보 조회 후 분석]
```

### 코드 비교
```
User: main과 develop 브랜치의 차이점을 보여줘
Claude: [git_diff 또는 github_compare 사용]
```

## 보안 고려사항

- GitHub Token은 환경 변수로 관리
- 읽기 전용 권한 우선 사용 (repo:read, pr:read)
- 로컬 파일 시스템 접근 제한
- 민감한 정보 로깅 방지

## 향후 계획

- [ ] GitHub Actions 워크플로우 조회
- [ ] 코드 리뷰 자동화 기능
- [ ] GitLab, Bitbucket 지원
- [ ] 커밋 메시지 템플릿 생성
- [ ] 코드 변경 통계 분석
- [ ] 브랜치 전략 추천

## 기여 방법

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 라이선스

MIT License

## 코드 예시

### MCP 서버 기본 구조 (server.py)

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

app = Server("git-agent")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="git_log",
            description="Get commit history from a Git repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_path": {"type": "string"},
                    "limit": {"type": "number", "default": 10},
                    "branch": {"type": "string", "default": "HEAD"},
                },
                "required": ["repo_path"],
            },
        ),
        # ... 추가 도구들
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "git_log":
        # Git 로그 구현
        pass
    # ... 추가 도구 핸들러들

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## 참고 자료

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [GitHub REST API](https://docs.github.com/en/rest)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [GitPython Documentation](https://gitpython.readthedocs.io/)
