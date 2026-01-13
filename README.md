# JaneJase Backend (자네자세 백엔드)

**자네자세** 프로젝트의 백엔드 서비스입니다. FastAPI 프레임워크를 기반으로 구축되었으며, 사용자 인증, 데이터 처리 및 클라이언트와의 통신을 담당합니다.

## 🛠 기술 스택 (Tech Stack)

이 프로젝트는 다음과 같은 기술들을 사용합니다:

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - 현대적이고 빠른(고성능) 파이썬 웹 프레임워크
- **Server**: [Uvicorn](https://www.uvicorn.org/) - ASGI 서버 구현체
- **Database**: PostgreSQL (권장) / AsyncPG (비동기 데이터베이스 드라이버)
- **Authentication**: JWT (JSON Web Tokens) with `python-jose`, `passlib`
- **Validation**: Pydantic
- **Environment Management**: python-dotenv

## 📂 프로젝트 구조 (Project Structure)

`app/` 디렉토리 내의 주요 구조는 다음과 같습니다:

```
app/
├── api/          # API 라우트 및 엔드포인트 정의
├── core/         # 핵심 설정 (Config, Security 등)
├── db/           # 데이터베이스 연결 및 세션 관리
├── models/       # (예상) 데이터베이스 모델 정의
├── schemas/      # Pydantic 스키마 (요청/응답 모델)
├── services/     # 비즈니스 로직 처리
├── repositories/ # 데이터베이스 액세스 계층 (CRUD)
└── main.py       # 애플리케이션 진입점 (Entry Point)
```

## 🚀 시작하기 (Getting Started)

### 1. 필수 구성 요소 (Prerequisites)

- Python 3.9 이상
- PostgreSQL 데이터베이스 (로컬 또는 원격)

### 2. 설치 (Installation)

레포지토리를 클론하고 필요한 의존성을 설치합니다.

```bash
# 가상환경 생성 (선택 사항이지만 권장됨)
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate
# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. 환경 변수 설정 (Configuration)

루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 설정 환경에 맞게 작성해주세요.

```ini
# 예시 설정 (실제 값으로 변경 필요)
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. 서버 실행 (Run Server)

Uvicorn을 사용하여 서버를 실행합니다.

```bash
uvicorn app.main:app --reload
```

- 서버가 실행되면 `http://127.0.0.1:8000`에서 접근할 수 있습니다.
- API 문서는 `http://127.0.0.1:8000/docs` (Swagger UI)에서 확인할 수 있습니다.

## 🔑 주요 기능 (Features)

- **회원가입 및 로그인**: JWT 기반의 보안 인증 시스템
- **데이터베이스 연동**: 비동기 처리를 통한 고성능 DB 작업
- **API 문서화**: FastAPI의 자동 문서화 기능 제공
