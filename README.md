# JaneJase Backend (자네자세 백엔드)

**자네자세** 프로젝트의 백엔드 서비스입니다. FastAPI를 기반으로 구축된 고성능 비동기 API 서버로, 사용자 인증(OAuth) 및 자세 분석 데이터의 저장과 조회를 담당합니다.

## 🛠 기술 스택 (Tech Stack)

### Core
- **Language**: Python 3.9+
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (0.115.5)
- **Server**: [Uvicorn](https://www.uvicorn.org/) (ASGI Server)

### Database & Data
- **Database**: PostgreSQL
- **Driver**: [Asyncpg](https://magicstack.github.io/asyncpg/) (비동기 DB 드라이버)
- **Validation**: [Pydantic](https://docs.pydantic.dev/) (데이터 검증 및 설정 관리)

### Security & Auth
- **Authentication**: JWT (JSON Web Tokens)
- **OAuth**: Google Login (`authlib`)
- **Crypto**: `passlib[bcrypt]`, `python-jose`

---

## 📂 소스 구조 (Source Structure)

`app/` 디렉토리 위주의 프로젝트 구조입니다.

```bash
JaneJase_BACKEND/
├── app/
│   ├── api/             # API 라우터 (Endpoints)
│   ├── core/            # 핵심 설정 (Config, Exception, Logging)
│   ├── db/              # DB 연결 풀 및 초기화 로직
│   ├── repositories/    # DB 쿼리 수행 및 데이터 액세스 계층
│   ├── schemas/         # Pydantic 모델 (Request/Response DTO)
│   ├── services/        # 비즈니스 로직 (Auth, Pose 처리 등)
│   ├── utils/           # 유틸리티 함수
│   └── main.py          # 앱 진입점 (FastAPI 인스턴스 생성 및 미들웨어 설정)
├── .env                 # 환경 변수 설정
└── requirements.txt     # 파이썬 의존성 목록
```

### 📁 주요 디렉토리 설명
- **api**: 클라이언트의 요청을 받아 적절한 서비스로 전달하는 라우팅 계층입니다.
- **services**: 실제 비즈니스 로직을 처리하며, 필요한 경우 Repository를 호출합니다.
- **repositories**: 직접적인 SQL 쿼리 실행을 담당하여 데이터베이스와 통신합니다. (Asyncpg 사용)
- **schemas**: API 입출력 데이터의 포맷과 유효성을 검사하는 Pydantic 모델들이 위치합니다.

---

## 🌊 기본적인 소스 플로우 (Basic Source Flow)

1. **Request**: 클라이언트가 API 요청 (예: `/api/v1/pose/data`)
2. **Middleware**: CORS 처리 및 세션/인증 토큰 검사
3. **Router (`api/`)**: URL에 맞는 핸들러 함수 호출
4. **Service (`services/`)**: 비즈니스 로직 수행 (예: 데이터 가공, 권한 확인)
5. **Repository (`repositories/`)**: DB 쿼리 실행 (CRUD)
6. **Database**: PostgreSQL 데이터 조회/저장
7. **Response**: Pydantic Schema에 맞춰 JSON 응답 반환

---

## 🚀 동작 방법 (How to Run)

### 1. 환경 설정 (Prerequisites)
- Python 3.9 이상 설치
- PostgreSQL 서버 실행 중이어야 함

### 2. 설치 (Installation)
```bash
# 가상환경 생성 및 활성화
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 3. 환경 변수 (.env)
루트 디렉토리에 `.env` 파일을 생성합니다.
```ini
PROJECT_NAME="JaneJase API"
VERSION="0.1.0"
API_V1_STR="/api/v1"

# Database
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=janejase_db

# Security
JWT_SECRET=your_super_secret_key_change_this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### 4. 실행 (Run)
```bash
# 개발 모드 (Auto Reload)
uvicorn app.main:app --reload
```
서버는 기본적으로 `http://127.0.0.1:8000` 에서 실행됩니다.
- API 문서 (Swagger): `http://127.0.0.1:8000/docs`

---

## 🔑 주요 기능 설명 (Key Features)

### 1. 사용자 인증 (Google OAuth + JWT)
- 구글 계정을 통한 소셜 로그인 지원.
- 로그인 성공 시 JWT Access Token 발급.
- `auth_service.py`에서 OAuth 인증 흐름 처리.

### 2. 자세 데이터 관리
- **정자세 기준 데이터(StandardData)**: 사용자가 설정한 올바른 자세의 랜드마크 기준점 저장.
- **경고 이력(Pose Detection)**: 자세가 무너졌을 때의 감지 데이터 저장.
- `pose_service.py`를 통해 데이터 처리 및 통계 로직 수행.

---

## 🎨 스타일링 및 코드 관리
- **Code Style**: PEP8 준수 권장.
- **Type Hinting**: Python Type Hints를 적극 사용하여 코드 가독성 및 안정성 확보.
- **Async I/O**: `async def` 및 `await` 키워드를 사용하여 비동기 처리 효율 극대화.

---

## 📝 개발 가이드 (Development Guide)
1. **새로운 API 추가**: `app/api/endpoints/`에 파일 생성 후 `app/api/router.py`에 등록.
2. **DB 스키마 변경**: `app/db/` 내의 초기화 스크립트 또는 마이그레이션 도구 활용.
3. **에러 처리**: `app/core/exceptions.py`에 정의된 예외 클래스 사용 권장.
