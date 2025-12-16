# Git Agent MCP Server

MCP(Model Context Protocol) 서버로, Git 저장소와 GitHub API를 통해 커밋 내역을 조회할 수 있는 도구를 제공합니다.

## 주요 기능

### Git Tools (로컬)
- **get_recent_commits**: 로컬 Git 저장소의 최근 커밋 내역 조회
  - 커밋 SHA, 작성자, 이메일, 날짜, 메시지 정보 제공
  - 브랜치 지정 가능
  - 조회할 커밋 개수 지정 가능

### GitHub Tools (원격)
- **get_recent_github_commits**: GitHub 저장소의 최근 커밋 내역 조회
  - Public/Private 저장소 지원 (Private는 토큰 필요)
  - 브랜치 지정 가능
  - 커밋 SHA, 작성자, 날짜, 메시지 정보 제공

## 설치 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd git-agent
```

### 2. 의존성 설치

```bash
pip install -e .
```

설치되는 패키지:
- `fastmcp` - MCP 서버 프레임워크
- `gitpython` - Git 저장소 조작
- `PyGithub` - GitHub REST API 클라이언트

## 프로젝트 구조

```
git-agent/
├── src/
│   └── git_mcp/
│       ├── __init__.py
│       ├── __main__.py          # MCP 서버 진입점
│       └── tools/
│           ├── __init__.py
│           ├── git_tools.py     # Git 관련 도구 (로컬)
│           └── github_tools.py  # GitHub 관련 도구 (원격)
├── tests/
│   ├── test_git_tools.py        # Git 도구 테스트
│   └── test_github_tools.py     # GitHub 도구 테스트
├── pyproject.toml               # 프로젝트 설정 및 의존성
├── README.md
└── .gitignore
```

## 실행 방법

### 개발/테스트 시 직접 실행

```bash
python -m git_mcp
```

### 설치 후 명령어로 실행

```bash
git-agent
```

## Claude Desktop 연동

### 1. 설정 파일 위치

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Mac:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### 2. 설정 내용 추가

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

**참고:**
- `cwd`: git-agent 프로젝트의 절대 경로로 수정
- `GITHUB_TOKEN`: GitHub Personal Access Token (옵셔널, Private 저장소 접근 시 필요)

### 3. Claude Desktop 재시작

설정 파일 저장 후 Claude Desktop을 완전히 종료하고 다시 실행합니다.

### 4. 연결 확인

Claude Desktop에서 다음과 같이 명령하여 도구가 로드되었는지 확인:

```
사용 가능한 도구 목록 보여줘
```

또는

```
이 저장소의 최근 커밋 보여줘: anthropics/anthropic-sdk-python
```

## 사용 예시

### 로컬 Git 저장소 조회

```
Claude에게: "c:\Users\username\projects\my-repo 저장소의 최근 5개 커밋 보여줘"
```

**도구 호출:**
```json
{
  "repo_path": "c:\\Users\\username\\projects\\my-repo",
  "count": 5
}
```

### GitHub 저장소 조회

```
Claude에게: "torvalds/linux 저장소의 main 브랜치 최근 10개 커밋 보여줘"
```

**도구 호출:**
```json
{
  "owner": "torvalds",
  "repo_path": "linux",
  "branch": "main",
  "count": 10
}
```

**응답 예시:**
```json
[
  {
    "sha": "abc1234",
    "author": "Linus Torvalds",
    "date": "2024-01-15T10:30:00Z",
    "message": "Merge branch 'for-linus' of git://..."
  }
]
```

## 테스트

### Git 도구 테스트

```bash
cd tests
python test_git_tools.py
```

### GitHub 도구 테스트

```bash
cd tests
python test_github_tools.py
```

## GitHub Token 생성 (옵셔널)

Private 저장소 접근이나 Rate Limit 증가를 위해 토큰 생성:

1. GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
2. "Generate new token" 클릭
3. 권한 선택:
   - `repo` (Private 저장소 접근)
   - `public_repo` (Public 저장소만)
4. 생성된 토큰을 Claude Desktop 설정의 `GITHUB_TOKEN`에 추가

**Rate Limits:**
- 토큰 없음: 60 requests/hour
- 토큰 있음: 5,000 requests/hour

## 기술 스택

- **Python 3.10+**
- **FastMCP** - MCP 서버 프레임워크
- **GitPython** - Git 저장소 조작
- **PyGithub** - GitHub REST API 클라이언트

## 문제 해결

### 서버 연결 안 됨

1. Claude Desktop의 Server Logs 확인:
   - 메뉴: `View > Developer > Server Logs`

2. 서버 수동 실행으로 에러 확인:
   ```bash
   cd c:\Users\YOUR_USERNAME\path\to\git-agent
   python -m git_mcp
   ```

3. 설정 파일 경로 확인:
   - `cwd` 경로가 올바른지 확인
   - 백슬래시 이스케이프 (`\\`) 확인

### Import 에러

패키지 재설치:
```bash
pip uninstall git-agent
pip install -e .
```

## 개발

### 의존성 추가

`pyproject.toml` 파일의 `dependencies` 섹션에 추가 후:

```bash
pip install -e .
```

### 코드 스타일

- PEP 8 준수
- Type hints 사용 권장

## 라이선스

MIT License

## 기여

Pull Request를 환영합니다!
