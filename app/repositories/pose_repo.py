import asyncpg
import json
from typing import Optional
from app.schemas.pose import StandardData, ViewWarning

async def create_pose(conn: asyncpg.Connection, pose_data: StandardData) -> str:
    """새로운 포즈 생성

    Args:
        conn: 데이터베이스 연결 객체
        pose_data: 생성할 포즈 정보 (StandardData 스키마)

    Returns:
        생성된 포즈 ID

    Raises:
        asyncpg.exceptions.UniqueViolationError: 포즈가 이미 존재하는 경우
    """
    row = await conn.fetchrow(
        """
        INSERT INTO pose (user_id, ended_at, measurement)
        VALUES ($1, $2, $3)
        RETURNING id
        """,
        pose_data.user_id,
        pose_data.ended_at,
        json.dumps(pose_data.measurement)
    )
    return str(row["id"]) if row else None


async def create_warning(conn: asyncpg.Connection,  view_warning: ViewWarning) -> dict:
    """새로운 경고 생성

    Args:
        conn: 데이터베이스 연결 객체
        view_warning: 생성할 경고 정보 (ViewWarning 스키마)

    Returns:
        생성된 경고 ID
    """
    print("view_warning : ", view_warning)
    
    # Insert new detection
    row = await conn.fetchrow(
        """
        INSERT INTO pose_detected (pose_id, occurred_at, duration_sec, avg_delta_ntsd, avg_delta_etsd, avg_delta_sld, status)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id
        """,
        view_warning.pose_id,
        view_warning.timestamp,
        view_warning.duration,
        view_warning.averages.get("FNTSD", 0.0),
        view_warning.averages.get("FETSD", 0.0),
        view_warning.averages.get("FSLD", 0.0),
        json.dumps(view_warning.status) 
    )
    
    if not row:
        return None

    # Get cumulative stats for this session (pose_id)
    stats = await conn.fetchrow(
        """
        SELECT count(*) as count, COALESCE(sum(duration_sec), 0) as total_time
        FROM pose_detected
        WHERE pose_id = $1
        """,
        view_warning.pose_id
    )
    
    return {"count": stats["count"], "total_time": stats["total_time"]}
