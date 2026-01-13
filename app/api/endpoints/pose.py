import asyncpg
import json
from typing import Any
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from asyncpg import Connection
from app.db.database import get_db
from app.services import pose_service
from app.schemas.pose import StandardData, ViewWarning
from app.repositories import pose_repo


router = APIRouter()

@router.post("/create")
async def create_pose(
    data: StandardData,
    db: Connection = Depends(get_db)
):
    # Fix recursion: call repo function instead of self
    row_id = await pose_repo.create_pose(db, data)
        
    if not row_id:
        raise HTTPException(status_code=500, detail="Failed to create pose")
            
    return {"id": row_id}

@router.post("/warning")
async def create_warning(
    data: ViewWarning,
    db: Connection = Depends(get_db)
):
    print("data : ", data)
    try:
        result = await pose_repo.create_warning(db, data)
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create warning")
            
        return {"count": result["count"], "total_time": result["total_time"]}
        
    except Exception as e:
        print(f"Error creating warning: {e}")
        raise HTTPException(status_code=500, detail=str(e))