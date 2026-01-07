from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
import asyncpg

from app.db.database import get_db
from app.services import auth_service
from app.schemas.user import UserResponse
from app.core.config import settings

router = APIRouter()

@router.get("/login/google")
async def google_login(request: Request):
    """구글 OAuth 로그인 시작

    사용자를 구글 로그인 페이지로 리디렉션합니다.
    구글에서 인증 완료 후 /auth/callback/google로 콜백됩니다.

    Flow:
        1. 사용자가 이 엔드포인트 호출
        2. 구글 로그인 페이지로 리디렉션
        3. 사용자가 구글에서 로그인
        4. 구글이 /auth/callback/google로 콜백

    Returns:
        구글 OAuth 인증 페이지로의 리디렉션 응답
    """
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await auth_service.oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback/google")
async def google_callback(request: Request, db: asyncpg.Connection = Depends(get_db)):
    """구글 OAuth 콜백 처리

    구글 인증 완료 후 호출되는 엔드포인트입니다.
    액세스 토큰을 받아 사용자 정보를 조회하고, 로그인/회원가입을 처리한 후
    JWT 토큰을 URL 파라미터로 프론트엔드로 리디렉트합니다.

    Flow:
        1. 구글로부터 인증 코드 수신
        2. 인증 코드로 액세스 토큰 교환
        3. 액세스 토큰으로 사용자 정보 조회
        4. DB에서 사용자 조회/생성
        5. JWT 토큰 발급
        6. 프론트엔드로 리디렉트 (token을 쿼리 파라미터로 전달)

    Args:
        request: FastAPI Request 객체 (OAuth state 포함)
        db: 데이터베이스 연결 객체 (의존성 주입)

    Returns:
        RedirectResponse: 프론트엔드 callback 페이지로 리디렉트

    Raises:
        HTTPException: OAuth 인증 실패 또는 사용자 정보 조회 실패 시
    """
    try:
        # 1. 구글로부터 액세스 토큰 받기
        token = await auth_service.oauth.google.authorize_access_token(request)
        access_token = token.get('access_token')

        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get access token")

        # 2. 구글 API로 사용자 정보 조회
        user_info = await auth_service.get_google_user_info(access_token)

        # 3. 로그인 또는 회원가입 처리
        user = await auth_service.login_or_register_oauth_user(
            conn=db,
            email=user_info['email'],
            name=user_info.get('name', ''),
            picture=user_info.get('picture', ''),
            provider='google'
        )

        # 4. JWT 토큰 생성
        jwt_token = auth_service.create_access_token(data={"sub": str(user['id'])})

        # 5. 프론트엔드로 리디렉트 (token을 쿼리 파라미터로 전달)
        frontend_url = settings.FRONTEND_URL or "http://localhost:7010"
        redirect_url = f"{frontend_url}/auth/callback?token={jwt_token}"
        return RedirectResponse(url=redirect_url)

    except Exception as e:
        # 에러 발생 시 프론트엔드 로그인 페이지로 리디렉트
        frontend_url = settings.FRONTEND_URL or "http://localhost:7010"
        error_url = f"{frontend_url}/login?error={str(e)}"
        return RedirectResponse(url=error_url)

@router.get("/me", response_model=UserResponse)
async def get_current_user(request: Request, db: asyncpg.Connection = Depends(get_db)):
    """현재 로그인한 사용자 정보 조회

    Authorization 헤더의 JWT 토큰을 검증하고 사용자 정보를 반환합니다.

    Headers:
        Authorization: Bearer {JWT_TOKEN}

    Args:
        request: FastAPI Request 객체
        db: 데이터베이스 연결 객체 (의존성 주입)

    Returns:
        UserResponse: 현재 로그인한 사용자 정보

    Raises:
        HTTPException 401: 토큰이 없거나 유효하지 않은 경우
        HTTPException 404: 사용자를 찾을 수 없는 경우

    Example:
        >>> headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJh..."}
        >>> response = requests.get("/auth/me", headers=headers)
    """
    # 1. Authorization 헤더에서 토큰 추출
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

    token = auth_header.split(' ')[1]

    # 2. 토큰 검증 및 사용자 ID 추출
    user_id = auth_service.verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # 3. DB에서 사용자 조회
    from app.repositories import user_repo
    user = await user_repo.find_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # UUID를 문자열로 변환
    user_dict = dict(user)
    user_dict['id'] = str(user_dict['id'])

    return UserResponse(**user_dict)
