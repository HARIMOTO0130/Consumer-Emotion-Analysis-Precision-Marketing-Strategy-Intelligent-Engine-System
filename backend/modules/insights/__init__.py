from fastapi import APIRouter
from .services import InsightsService

router = APIRouter(prefix="/insights", tags=["洞察分析"])

@router.get("/")
async def get_insights():
    return await InsightsService.get_insights_data()

@router.get("/detailed")
async def get_detailed_insights():
    return await InsightsService.get_detailed_insights()