from core.database import database
from .models import emotion_distribution_table
from typing import List, Dict, Any
import logging
from core.enum_mapping import get_mapped_value, CHANNEL_MAP

logger = logging.getLogger(__name__)

class EmotionDistributionService:
    @staticmethod
    async def get_distribution_data() -> List[Dict[str, Any]]:
        try:
            query = emotion_distribution_table.select()
            results = await database.fetch_all(query)
            return [
                {
                    "channel": get_mapped_value(CHANNEL_MAP, dict(r).get("channel")),
                    "positive": dict(r).get("positive"),
                    "negative": dict(r).get("negative"),
                    "positivePercent": float(dict(r).get("positive_percent", 0.0))
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Failed to fetch emotion distribution: {str(e)}", exc_info=True)
            return []