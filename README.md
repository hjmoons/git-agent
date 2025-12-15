# Git Agent MCP Server

MCP(Model Context Protocol) 서버로, 로컬 Git 저장소의 커밋 내역을 조회할 수 있는 도구를 제공합니다.

## 주요 기능

- **get_recent_commits**: 로컬 Git 저장소의 최근 커밋 내역 조회
  - 커밋 SHA, 작성자, 날짜, 메시지 정보 제공
  - 조회할 커밋 개수 지정 가능

## 설치 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd git-agent
```

### 2. 가상환경 생성 및 활성화

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. 의존성 설치

```bash
pip install -e .
```

## 실행 방법

### MCP 서버 실행

```bash
cd src/app
python server.py
```

서버는 `http://127.0.0.1:8080`에서 실행됩니다.

### 기능 테스트

```bash
cd test
python test_git_tools.py
```

## 프로젝트 구조

```
git-agent/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── server.py          # MCP 서버 진입점
│       └── tools/
│           ├── __init__.py
│           └── git_tools.py   # Git 관련 도구 구현
├── test/
│   └── test_git_tools.py      # 기능 테스트 스크립트
├── pyproject.toml             # 프로젝트 설정 및 의존성
├── README.md
└── .gitignore
```

## 사용 예시

MCP 클라이언트에서 `get_recent_commits` 도구를 호출하여 커밋 내역을 조회할 수 있습니다.

```python
# 예시: 최근 5개 커밋 조회
{
  "repo_path": "/path/to/your/repo",
  "count": 5
}
```

**응답 예시:**
```json
[
  {
    "sha": "abc123def456...",
    "author": "홍길동",
    "date": "2024-01-15T10:30:00+09:00",
    "message": "Initial commit"
  },
  ...
]
```

## 기술 스택

- **Python 3.10+**
- **FastMCP** - MCP 서버 프레임워크
- **GitPython** - Git 저장소 조작

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
