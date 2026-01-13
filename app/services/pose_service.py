import asyncpg
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from authlib.integrations.starlette_client import OAuth
import httpx

from app.core.exceptions import bad_request, unauthorized
from app.repositories import user_repo
from app.core.config import settings
from app.schemas.user import UserCreate, UserResponse

# OAuth 클라이언트 설정
oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT 액세스 토큰 생성

    사용자 정보를 담은 JWT 토큰을 생성합니다.

    Args:
        data: 토큰에 포함할 데이터 (일반적으로 {"sub": user_id})
        expires_delta: 토큰 만료 시간 (기본값: 설정에서 가져옴)

    Returns:
        인코딩된 JWT 토큰 문자열

    Example:
        >>> token = create_access_token({"sub": "user-uuid-123"})
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """JWT 토큰 검증 및 사용자 ID 추출

    토큰을 검증하고 페이로드에서 사용자 ID를 추출합니다.

    Args:
        token: 검증할 JWT 토큰 문자열

    Returns:
        사용자 ID (UUID 문자열) 또는 None (토큰이 유효하지 않은 경우)

    Raises:
        JWTError: 토큰 디코딩 실패 시 (내부적으로 처리됨)
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        return user_id
    except JWTError:
        return None


async def get_google_user_info(access_token: str) -> dict:
    """구글 OAuth 액세스 토큰으로 사용자 정보 조회

    구글 API를 호출하여 사용자 프로필 정보를 가져옵니다.

    Args:
        access_token: 구글 OAuth 액세스 토큰

    Returns:
        사용자 정보 딕셔너리
        - email: 이메일 주소
        - name: 사용자 이름
        - picture: 프로필 이미지 URL

    Raises:
        HTTPException: API 호출 실패 시
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            'https://www.googleapis.com/oauth2/v2/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        response.raise_for_status()
        return response.json()


async def login_or_register_oauth_user(conn: asyncpg.Connection, email: str, name: str, picture: str, provider: str) -> dict:
    """OAuth 로그인 또는 회원가입 처리

    이메일로 기존 사용자를 조회하고, 없으면 새로 생성합니다.
    구글/카카오 로그인 시 자동으로 회원가입이 진행됩니다.

    Args:
        conn: 데이터베이스 연결 객체
        email: 사용자 이메일
        name: 사용자 이름
        picture: 프로필 이미지 URL
        provider: OAuth 제공자 (google 또는 kakao)

    Returns:
        사용자 정보 딕셔너리 (기존 사용자 또는 새로 생성된 사용자)

    Example:
        >>> user = await login_or_register_oauth_user(
        ...     conn, "user@example.com", "홍길동", "https://...", "google"
        ... )
    """
    # 기존 사용자 조회
    existing_user = await user_repo.find_by_email(conn, email)

    if existing_user:
        return existing_user

    # 신규 사용자 생성
    user_data = UserCreate(
        email=email,
        name=name,
        picture=picture,
        provider=provider
    )
    new_user = await user_repo.create_user(conn, user_data)
    return new_user