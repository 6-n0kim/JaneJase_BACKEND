from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Any

class StandardData(BaseModel):
    user_id: UUID
    ended_at: datetime | None = None
    measurement: dict[str, Any]

class ViewWarning(BaseModel):
    pose_id: UUID
    timestamp: datetime
    duration: float
    status: dict[str, Any]
    averages: dict[str, Any]

class pose_detected(BaseModel):
    pose_id : UUID
    occurred_at : datetime
    duration_sec : float
    avg_delta_ntsd : float
    avg_delta_etsd : float
    avg_delta_sld : float
    status : dict[str, Any]

class pose_detected(BaseModel):
    pose_id : UUID
    occurred_at : datetime
    duration_sec : float
    avg_delta_ntsd : float
    avg_delta_etsd : float
    avg_delta_sld : float
    status : dict[str, Any]

    