import asyncpg

from app.core.config import settings

# Global connection pool
_pool: asyncpg.Pool | None = None


async def init_db_pool() -> None:
    """Initialize database connection pool

    Note: statement_cache_size=0 is required when using pgbouncer with
    pool_mode set to "transaction" or "statement" mode.
    """
    global _pool
    _pool = await asyncpg.create_pool(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
        min_size=2,
        max_size=10,
        command_timeout=60,
        statement_cache_size=0,  # Required for pgbouncer compatibility
    )
    print(f"데이터베이스 연결 성공: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")


async def close_db_pool() -> None:
    """Close database connection pool"""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
        print("데이터베이스 연결 종료")


def get_pool() -> asyncpg.Pool:
    """Get the database connection pool"""
    if _pool is None:
        raise RuntimeError("Database pool is not initialized. Call init_db_pool() first.")
    return _pool


async def get_db() -> asyncpg.Connection:
    """
    Dependency to get database connection.
    Usage in FastAPI endpoint:
        async def endpoint(db: asyncpg.Connection = Depends(get_db)):
    """
    pool = get_pool()
    async with pool.acquire() as conn:
        yield conn


async def init_schema() -> None:
    """데이터베이스 테이블 스키마 초기화 함수

    users 테이블 생성:
    - id: 기본 키 (UUID)
    - email: 사용자 이메일 (고유값)
    - name: 사용자 이름
    - picture: 프로필 이미지 URL
    - provider: OAuth 제공자 (google, kakao 등)
    - created_at: 생성 시간
    """
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                email VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(100),
                picture TEXT,
                provider VARCHAR(50) NOT NULL,
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
    print("데이터베이스 스키마 초기화 완료")