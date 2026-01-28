from fastapi import APIRouter
from .services import EmotionDistributionService

router = APIRouter(prefix="/emotion-distribution", tags=["情绪分布"])

@router.get("/")
async def get_emotion_distribution():
    return await EmotionDistributionService.get_distribution_data()