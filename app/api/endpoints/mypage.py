from fastapi import APIRouter, Depends, HTTPException
from asyncpg import Connection
from uuid import UUID
from app.db.database import get_db
from app.repositories import mypage_repo

router = APIRouter()

@router.get("/history/{user_id}")
async def get_history(
    user_id: UUID,
    db: Connection = Depends(get_db)
):
    try:
        history = await mypage_repo.get_mypage_history(db, user_id)
        return history
    except Exception as e:
        print(f"Error fetching history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/history/{pose_id}")
async def delete_history(
    pose_id: UUID,
    db: Connection = Depends(get_db)
):
    try:
        success = await mypage_repo.delete_mypage_history(db, pose_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"result": "success"}
    except Exception as e:
        print(f"Error deleting history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
