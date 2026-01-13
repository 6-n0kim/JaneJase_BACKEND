import asyncpg
from typing import List, Dict, Any
from uuid import UUID

async def get_mypage_history(conn: asyncpg.Connection, user_id: UUID) -> List[Dict[str, Any]]:
    """사용자의 교정 세션 히스토리 조회

    Args:
        conn: 데이터베이스 연결 객체
        user_id: 사용자 ID

    Returns:
        세션 리스트 (날짜, 경고 횟수, 총 시간)
    """
    rows = await conn.fetch(
        """
        SELECT 
            p.id as pose_id,
            p.created_at,
            COUNT(pd.id) as warning_count,
            COALESCE(SUM(pd.duration_sec), 0) as total_unfocus_time
        FROM pose p
        LEFT JOIN pose_detected pd ON p.id = pd.pose_id
        WHERE p.user_id = $1
        GROUP BY p.id, p.created_at
        ORDER BY p.created_at DESC
        """,
        user_id
    )
    
    return [
        {
            "pose_id": str(row["pose_id"]),
            "created_at": row["created_at"],
            "warning_count": row["warning_count"],
            "total_unfocus_time": row["total_unfocus_time"]
        }
        for row in rows
    ]

async def delete_mypage_history(conn: asyncpg.Connection, pose_id: UUID) -> bool:
    """교정 세션 삭제

    Args:
        conn: 데이터베이스 연결 객체
        pose_id: 포즈 ID

    Returns:
        성공 여부
    """
    # pose_detected는 cascade 삭제가 설정되어 있다고 가정하거나, 아니면 여기서 먼저 삭제해야 함.
    # 일단 pose_detected도 같이 삭제하는 로직 추가
    await conn.execute("DELETE FROM pose_detected WHERE pose_id = $1", pose_id)
    result = await conn.execute("DELETE FROM pose WHERE id = $1", pose_id)
    return result == "DELETE 1"
