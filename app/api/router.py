from fastapi import APIRouter
from app.api.endpoints import health, auth, pose, mypage

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(pose.router, prefix="/pose", tags=["pose"])
api_router.include_router(mypage.router, prefix="/mypage", tags=["mypage"])
