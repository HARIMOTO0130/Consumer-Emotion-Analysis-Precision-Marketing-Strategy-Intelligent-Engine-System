from fastapi import APIRouter
from .services import TrendInsightsService

router = APIRouter(prefix="/trend-insights", tags=["趋势洞察"])

@router.get("/")
async def get_trend_insights():
    return await TrendInsightsService.get_trend_insights()