from fastapi import APIRouter
from .services import AlertsService

router = APIRouter(prefix="/alerts", tags=["风险预警"])

@router.get("/")
async def get_alerts():
    return await AlertsService.get_alerts()