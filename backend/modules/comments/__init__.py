from fastapi import APIRouter, Query
from .services import CommentsService

router = APIRouter(prefix="/comments", tags=["评论管理"])

@router.get("/recent")
async def get_recent_comments(limit: int = Query(5, description="评论数量")):
    return await CommentsService.get_recent_comments(limit)

@router.get("/detailed")
async def get_detailed_comments():
    return await CommentsService.get_detailed_comments()