from datetime import datetime, timedelta
from typing import List, Dict, Any
from core.database import database
from .models import stats_table
import logging

logger = logging.getLogger(__name__)

class StatsService:
    @staticmethod
    async def get_stats_data(time_range: str = "30d") -> Dict[str, Any]:
        try:
            query = stats_table.select().limit(1)
            result = await database.fetch_one(query)
            
            if not result:
                logger.warning("No stats data found in database")
                return {
                    "totalReviews": 0,
                    "positiveCount": 0,
                    "negativeCount": 0,
                    "positiveRate": 0.0,
                    "trendChange": 0.0,
                    "alertCount": 0,
                    "hotTopicCount": 0,
                    "topTopic": "",
                    "updatedAt": ""
                }
            
            row = dict(result)
            return {
                "totalReviews": row.get("total_reviews", 0),
                "positiveCount": row.get("positive_count", 0),
                "negativeCount": row.get("negative_count", 0),
                "positiveRate": float(row.get("positive_rate", 0.0)),
                "trendChange": float(row.get("trend_change", 0.0)),
                "alertCount": row.get("alert_count", 0),
                "hotTopicCount": row.get("hot_topic_count", 0),
                "topTopic": row.get("top_topic", ""),
                "updatedAt": row.get("updated_at", "")
            }
        except Exception as e:
            logger.error(f"Failed to fetch stats: {e}", exc_info=True)
            return {
                "totalReviews": 0,
                "positiveCount": 0,
                "negativeCount": 0,
                "positiveRate": 0.0,
                "trendChange": 0.0,
                "alertCount": 0,
                "hotTopicCount": 0,
                "topTopic": "",
                "updatedAt": ""
            }