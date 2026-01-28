from fastapi import APIRouter, Query
from .services import StatsService

router = APIRouter(prefix="/stats", tags=["统计概览"])

@router.get("/")
async def get_stats(time_range: str = Query("24h", description="时间范围")):
    return await StatsService.get_stats_data(time_range)