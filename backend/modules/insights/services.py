from typing import List, Dict, Any
import logging
from core.database import database
from .models import insights_table
from core.enum_mapping import (
    get_mapped_value,
    INSIGHT_TYPE_MAP,
    PRIORITY_MAP,
    ACTION_TEXT_MAP
)

logger = logging.getLogger(__name__)

class InsightsService:
    @staticmethod
    async def get_insights_data() -> List[Dict[str, Any]]:
        try:
            query = insights_table.select().limit(3)
            results = await database.fetch_all(query)
            
            insights_list = []
            for r in results:
                record = dict(r)
                insights_list.append({
                    "id": record.get("id"),
                    "type": get_mapped_value(INSIGHT_TYPE_MAP, record.get("type")),
                    "date": record["date"].isoformat() if record.get("date") else None,
                    "text": record.get("text"),
                    "action": record.get("action"),
                    "actionText": get_mapped_value(ACTION_TEXT_MAP, record.get("action_text")) 
                })
            return insights_list
        except Exception as e:
            logger.error(f"Failed to fetch insights data: {str(e)}", exc_info=True)
            return []

    @staticmethod
    async def get_detailed_insights() -> List[Dict[str, Any]]:
        try:
            query = insights_table.select().limit(3)
            results = await database.fetch_all(query)
            
            detailed_insights_list = []
            for r in results:
                record = dict(r)
                detailed_insights_list.append({
                    "id": record.get("id"),
                    "title": record.get("title"),
                    "description": record.get("description"),
                    "recommendation": record.get("recommendation"),
                    "priority": get_mapped_value(PRIORITY_MAP, record.get("priority")),
                    "expectedOutcome": record.get("expected_outcome"),
                    "action": record.get("action"),
                    "actionText": get_mapped_value(ACTION_TEXT_MAP, record.get("action_text"))
                })
            return detailed_insights_list
        except Exception as e:
            logger.error(f"Failed to fetch detailed insights: {str(e)}", exc_info=True)
            return []