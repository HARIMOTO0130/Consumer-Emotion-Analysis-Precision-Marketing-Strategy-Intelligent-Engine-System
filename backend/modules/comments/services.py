from core.database import database
from typing import List, Dict, Any
from .models import comments_table
import logging
from core.enum_mapping import (
    get_mapped_value,
    CHANNEL_MAP,
    EMOTION_MAP,
    INTENSITY_MAP
)

logger = logging.getLogger(__name__)

class CommentsService:
    @staticmethod
    async def get_recent_comments(limit: int = 5) -> List[Dict[str, Any]]:
        try:
            query = comments_table.select().order_by(comments_table.c.id.desc()).limit(limit)
            results = await database.fetch_all(query)
            return [
                {
                    "id": dict(r).get("id"),
                    "text": dict(r).get("text"),
                    "source": get_mapped_value(CHANNEL_MAP, dict(r).get("source")),
                    "time": dict(r).get("time"),
                    "emotion": get_mapped_value(EMOTION_MAP, dict(r).get("emotion"))
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Failed to fetch recent comments: {str(e)}", exc_info=True)
            return []

    @staticmethod
    async def get_detailed_comments() -> List[Dict[str, Any]]:
        try:
            query = comments_table.select().order_by(comments_table.c.id.desc()).limit(10)
            results = await database.fetch_all(query)
            
            return [
                {
                    "text": dict(r).get("text"),
                    "source": get_mapped_value(CHANNEL_MAP, dict(r).get("source")),
                    "sentiment": get_mapped_value(EMOTION_MAP, dict(r).get("sentiment")),
                    "intensity": get_mapped_value(INTENSITY_MAP, dict(r).get("intensity")),
                    "timestamp": dict(r)["timestamp"].isoformat() if dict(r).get("timestamp") else None
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Failed to fetch detailed comments: {str(e)}", exc_info=True)
            return []