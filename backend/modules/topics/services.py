from core.database import database
from .models import topics_table
from typing import List, Dict, Any
import logging
from core.enum_mapping import (
    get_mapped_value,
    TOPIC_NAME_MAP,
    EMOTION_MAP,
    TREND_MAP
)

logger = logging.getLogger(__name__)

class TopicsService:
    @staticmethod
    async def get_topics() -> List[Dict[str, Any]]:
        try:
            query = topics_table.select()
            results = await database.fetch_all(query)
            return [
                {
                    "rank": dict(r).get("rank"),
                    "name": get_mapped_value(TOPIC_NAME_MAP, dict(r).get("name")),
                    "mentions": dict(r).get("mentions"),
                    "sentiment": get_mapped_value(EMOTION_MAP, dict(r).get("sentiment")),
                    "trend": get_mapped_value(TREND_MAP, dict(r).get("trend"))
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Failed to fetch topics: {str(e)}", exc_info=True)
            return []