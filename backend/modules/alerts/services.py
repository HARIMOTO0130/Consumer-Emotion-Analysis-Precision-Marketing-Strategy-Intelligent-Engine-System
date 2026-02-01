from core.database import database
from .models import alerts_table
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AlertsService:
    @staticmethod
    async def get_alerts() -> List[Dict[str, Any]]:
        try:
            query = alerts_table.select()
            results = await database.fetch_all(query)
            return [
                {
                    "id": dict(r).get("id"),
                    "title": dict(r).get("title"),
                    "type": dict(r).get("type"),
                    "severity": dict(r).get("severity"),
                    "date": dict(r).get("date"),
                    "status": dict(r).get("status")
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Failed to fetch alerts: {str(e)}", exc_info=True)
            return []