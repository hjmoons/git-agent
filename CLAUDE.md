# Git Agent MCP Server

MCP(Model Context Protocol) 서버로, GitHub와 Git 저장소 관리를 위한 다양한 기능을 제공합니다.

## 프로젝트 개요

이 프로젝트는 Claude 및 다른 AI 어시스턴트가 Git 저장소와 상호작용할 수 있도록 하는 MCP 서버입니다. 커밋 내역 조회, PR 관리, 소스코드 비교 등의 기능을 제공합니다.

## 주요 기능

### Git 기능 (로컬)
- **커밋 내역 조회**: 로컬 저장소의 커밋 히스토리 확인
- **브랜치 관리**: 브랜치 생성, 삭제, 목록 조회 (향후 추가 예정)
- **diff/비교**: 커밋 간, 브랜치 간 코드 변경사항 비교 (향후 추가 예정)
- **로그 분석**: Git 로그 필터링 및 검색
- **상태 확인**: 워킹 디렉토리 및 스테이징 영역 상태 (향후 추가 예정)

### GitHub 기능 (원격)
- **커밋 내역 조회**: GitHub 저장소의 커밋 히스토리 조회
- **Pull Request 관리** (향후 추가 예정)
  - PR 목록 조회
  - PR 상세 정보 확인
  - PR diff 조회
  - 리뷰 코멘트 조회
- **Issue 관리** (향후 추가 예정)
  - Issue 목록 및 상세 정보
- **저장소 정보** (향후 추가 예정)
  - 저장소 메타데이터
  - 기여자 정보
  - 릴리스 정보

## 기술 스택

- **언어**: Python 3.10+
- **프로토콜**: MCP (Model Context Protocol)
- **주요 라이브러리**:
  - `fastmcp` - MCP 서버 프레임워크
  - `PyGithub` - GitHub REST API 클라이언트
  - `GitPython` - Git 저장소 조작

## 프로젝트 구조

```
git-agent/
├── src/
│   └── git_mcp/
│       ├── __init__.py
│       ├── __main__.py          # MCP 서버 진입점
│       └── tools/               # MCP 도구 정의
│           ├── __init__.py
│           ├── git_tools.py     # Git 관련 도구 (로컬)
│           └── github_tools.py  # GitHub 관련 도구 (원격)
├── tests/                       # 테스트 코드
│   ├── __init__.py
│   ├── test_git_tools.py
│   └── test_github_tools.py
├── pyproject.toml               # 프로젝트 설정 및 의존성
├── README.md
├── CLAUDE.md
└── .env.example                 # 환경 변수 예시
```

## MCP Tools 설계

### Git Tools (로컬)

1. **get_recent_commits**
   - 로컬 Git 저장소의 최근 커밋 내역 조회
   - 입력: repo_path, count (기본 5), branch (옵셔널)
   - 출력: 커밋 리스트 (sha, author, email, date, message)

### GitHub Tools (원격)

1. **get_recent_github_commits**
   - GitHub 저장소의 커밋 내역 조회 (GitHub API 기반)
   - 입력: owner, repo_path, branch (옵셔널), count (기본 5)
   - 출력: 커밋 리스트 (sha, author, date, message)
   - Public 저장소는 토큰 없이 조회 가능

## 개발 가이드

### 환경 설정

```bash
# 저장소 클론
git clone <repository-url>
cd git-agent

# 의존성 설치
pip install -e .

# 개발 모드 실행
python -m git_mcp

# 설치 후 명령어로 실행
git-agent

# 테스트
pytest
```

### 환경 변수

```env
GITHUB_TOKEN=your_github_personal_access_token
```

**참고:**
- Public 저장소는 토큰 없이도 조회 가능
- Private 저장소 접근 시 토큰 필요
- 토큰 없으면 Rate Limit 60/hour, 있으면 5,000/hour

### 의존성 (pyproject.toml)

```toml
[project]
name = "git-agent"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastmcp",
    "gitpython",
    "PyGithub",
]

[project.scripts]
git-agent = "git_mcp.__main__:main"

[tool.setuptools.packages.find]
where = ["src"]
```

## Claude Desktop 연동

### 설정 파일 위치

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Mac:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### 설정 예시

```json
{
  "mcpServers": {
    "git-agent": {
      "command": "python",
      "args": ["-m", "git_mcp"],
      "cwd": "c:\\Users\\YOUR_USERNAME\\path\\to\\git-agent",
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**venv 사용 시:**

```json
{
  "mcpServers": {
    "git-agent": {
      "command": "c:\\path\\to\\git-agent\\venv\\Scripts\\python.exe",
      "args": ["-m", "git_mcp"]
    }
  }
}
```

**설치된 실행파일 사용:**

```json
{
  "mcpServers": {
    "git-agent": {
      "command": "c:\\path\\to\\git-agent\\venv\\Scripts\\git-agent.exe"
    }
  }
}
```

## AI Agent 애플리케이션에서 사용

MCP는 Claude Desktop 전용이 아닙니다. OpenAI GPT, Anthropic Claude API 등 어떤 LLM과도 연동 가능합니다.

### 기본 사용 예시

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def use_git_agent():
    # MCP 서버 연결
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "git_mcp"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 사용 가능한 도구 목록
            tools = await session.list_tools()

            # 도구 호출
            result = await session.call_tool(
                "get_recent_github_commits",
                {
                    "owner": "torvalds",
                    "repo_path": "linux",
                    "count": 10
                }
            )

            print(result)
```

### 서버 배포 시나리오

```bash
# 서버에 설치
cd /opt/git-agent
git clone <repository-url> .
pip install -e .

# Agent 애플리케이션에서 사용
# (동일한 서버 내에서 stdio 통신)
```

### 활용 사례

1. **코드 리뷰 자동화**
   - PR 생성 시 자동 보안/성능 검사
   - 코딩 컨벤션 준수 확인
   - 테스트 커버리지 검증
   - 과거 버그 패턴 학습 및 경고

2. **커밋 분석**
   - 커밋 메시지 품질 검사
   - 변경사항 적절성 검토
   - 커밋 패턴 분석

3. **릴리스 노트 자동 생성**
   - 커밋 히스토리 기반 변경사항 요약
   - 버전별 주요 변경사항 정리

4. **코드베이스 인사이트**
   - 활발한 개발 영역 파악
   - 기여자 분석
   - 코드 변경 추세 분석

5. **보안 및 성능 리뷰**
   - OWASP Top 10 자동 체크
   - 민감 정보 노출 감지
   - N+1 쿼리, 메모리 누수 감지

## 사용 예시

### 로컬 Git 저장소 조회
```
User: c:\projects\my-repo 저장소의 최근 5개 커밋을 보여줘
Claude: [get_recent_commits 도구 사용하여 커밋 내역 표시]
```

### GitHub 저장소 조회
```
User: torvalds/linux 저장소의 최근 커밋 10개 보여줘
Claude: [get_recent_github_commits 도구로 커밋 조회]
```

### 코드 비교 (향후 추가 예정)
```
User: main과 develop 브랜치의 차이점을 보여줘
Claude: [git_diff 또는 github_compare 사용]
```

## 보안 고려사항

- GitHub Token은 환경 변수로 관리
- 읽기 전용 권한 우선 사용 (repo:read, pr:read)
- 로컬 파일 시스템 접근 제한
- 민감한 정보 로깅 방지
- Private 저장소 접근 시 적절한 권한 확인

## 향후 계획

- [ ] GitHub Pull Request 관리 도구
  - PR 목록, 상세 정보, 파일 변경 조회
  - PR diff, 리뷰 코멘트 조회
- [ ] GitHub Issue 관리
- [ ] GitHub Actions 워크플로우 조회
- [ ] 코드 리뷰 자동화 기능
- [ ] GitLab, Bitbucket 지원
- [ ] 커밋 메시지 템플릿 생성
- [ ] 코드 변경 통계 분석
- [ ] 브랜치 전략 추천

## 문제 해결

### MCP 서버 연결 실패

1. **Server Logs 확인**
   - Claude Desktop: `View > Developer > Server Logs`

2. **수동 실행으로 에러 확인**
   ```bash
   python -m git_mcp
   ```

3. **Import 에러**
   ```bash
   pip uninstall git-agent
   pip install -e .
   ```

4. **경로 문제**
   - `cwd` 경로가 올바른지 확인
   - Windows: 백슬래시 이스케이프 (`\\`) 필요

## 기여 방법

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 라이선스

MIT License

## 참고 자료

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [GitHub REST API](https://docs.github.com/en/rest)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [GitPython Documentation](https://gitpython.readthedocs.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
