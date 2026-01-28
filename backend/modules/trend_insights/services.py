from core.database import database
from .models import trend_insights_table
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class TrendInsightsService:
    @staticmethod
    async def get_trend_insights() -> List[Dict[str, Any]]:
        try:
            query = trend_insights_table.select()
            results = await database.fetch_all(query)
            return [{"id": r["id"], "text": r["text"]} for r in results]
        except Exception as e:
            logger.error(f"Failed to fetch trend insights: {e}")
            return []
    
    get_data = get_trend_insights