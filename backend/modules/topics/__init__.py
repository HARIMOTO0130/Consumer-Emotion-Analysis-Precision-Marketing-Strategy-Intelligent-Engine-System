from fastapi import APIRouter
from .services import TopicsService

router = APIRouter(prefix="/topics", tags=["热点话题"])

@router.get("/")
async def get_topics():
    return await TopicsService.get_topics()