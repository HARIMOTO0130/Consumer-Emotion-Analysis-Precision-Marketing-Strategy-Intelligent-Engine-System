from fastapi import APIRouter
from .services import MarketingService
router = APIRouter(prefix="/marketing", tags=["营销"])

@router.get("/activities")
async def read_marketing():
    return await MarketingService.get_activities_data()