from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """사용자 기본 스키마

    Attributes:
        email: 사용자 이메일 (유효성 검사 포함)
        name: 사용자 이름 (선택 사항)
    """
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    """사용자 생성 스키마

    OAuth 로그인 시 사용되는 스키마

    Attributes:
        picture: 프로필 이미지 URL (선택 사항)
        provider: OAuth 제공자 (google, kakao 등)
    """
    picture: Optional[str] = None
    provider: str

class UserResponse(UserBase):
    """사용자 응답 스키마

    API 응답 시 사용되는 스키마

    Attributes:
        id: 사용자 고유 ID (UUID)
        picture: 프로필 이미지 URL
        provider: OAuth 제공자
        created_at: 계정 생성 시간
    """
    id: str
    picture: Optional[str] = None
    provider: str
    created_at: datetime

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """로그인 응답 스키마

    로그인 성공 시 반환되는 스키마

    Attributes:
        access_token: JWT 액세스 토큰
        token_type: 토큰 타입 (일반적으로 "bearer")
        user: 로그인한 사용자 정보
    """
    access_token: str
    token_type: str
    user: UserResponse
