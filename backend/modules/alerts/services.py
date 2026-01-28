from core.database import database
from .models import alerts_table
from typing import List, Dict, Any
import logging
from core.enum_mapping import (
    get_mapped_value,
    PRIORITY_MAP,
    ALERT_STATUS_MAP
)

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
                    "severity": get_mapped_value(PRIORITY_MAP, dict(r).get("severity")),
                    "date": dict(r)["date"].isoformat() if dict(r).get("date") else None,
                    "status": get_mapped_value(ALERT_STATUS_MAP, dict(r).get("status"))
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Failed to fetch alerts: {str(e)}", exc_info=True)
            return []