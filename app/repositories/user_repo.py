import asyncpg
from typing import Optional
from app.schemas.user import UserCreate


async def find_by_email(conn: asyncpg.Connection, email: str) -> Optional[dict]:
    """이메일로 사용자 조회

    Args:
        conn: 데이터베이스 연결 객체
        email: 조회할 사용자 이메일

    Returns:
        사용자 정보 딕셔너리 또는 None (사용자가 없는 경우)
    """
    row = await conn.fetchrow("SELECT * FROM users WHERE email = $1", email)
    return dict(row) if row else None


async def create_user(conn: asyncpg.Connection, user_data: UserCreate) -> dict:
    """새로운 사용자 생성

    Args:
        conn: 데이터베이스 연결 객체
        user_data: 생성할 사용자 정보 (UserCreate 스키마)

    Returns:
        생성된 사용자 정보 딕셔너리

    Raises:
        asyncpg.exceptions.UniqueViolationError: 이메일이 이미 존재하는 경우
    """
    row = await conn.fetchrow(
        """
        INSERT INTO users (email, name, picture, provider)
        VALUES ($1, $2, $3, $4)
        RETURNING *
        """,
        user_data.email,
        user_data.name,
        user_data.picture,
        user_data.provider,
    )
    return dict(row)


async def find_by_id(conn: asyncpg.Connection, user_id: str) -> Optional[dict]:
    """ID로 사용자 조회

    Args:
        conn: 데이터베이스 연결 객체
        user_id: 조회할 사용자 ID (UUID 문자열)

    Returns:
        사용자 정보 딕셔너리 또는 None (사용자가 없는 경우)
    """
    row = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    return dict(row) if row else None