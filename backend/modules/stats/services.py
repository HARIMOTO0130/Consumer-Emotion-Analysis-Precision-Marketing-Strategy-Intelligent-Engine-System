from datetime import datetime, timedelta
from typing import List, Dict, Any
from core.database import database
from .models import stats_table
import logging
from core.enum_mapping import get_mapped_value, TOP_TOPIC_MAP

logger = logging.getLogger(__name__)

class StatsService:
    @staticmethod
    async def get_stats_data(time_range: str = "30d") -> Dict[str, Any]:
        try:
            query = stats_table.select().order_by(stats_table.c.updated_at.desc()).limit(1)
            
            result = await database.fetch_one(query)
            if not result:
                return {}
            
            row = dict(result)
            return {
                "totalReviews": row.get("total_reviews"),
                "positiveCount": row.get("positive_count"),
                "negativeCount": row.get("negative_count"),
                "positiveRate": float(row.get("positive_rate", 0.0)),
                "trendChange": float(row.get("trend_change", 0.0)),
                "alertCount": row.get("alert_count"),
                "hotTopicCount": row.get("hot_topic_count"),
                "topTopic": get_mapped_value(TOP_TOPIC_MAP, row.get("top_topic")),
                "updatedAt": row["updated_at"].isoformat() if row.get("updated_at") else None
            }
        except Exception as e:
            logger.error(f"Failed to fetch stats: {e}")
            return {}
    
    get_data = get_stats_data