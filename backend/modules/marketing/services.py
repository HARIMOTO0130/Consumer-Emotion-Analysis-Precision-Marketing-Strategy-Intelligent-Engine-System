from core.database import database
from .models import marketing_activities_table
from typing import List, Dict, Any
import logging
from core.enum_mapping import (
    get_mapped_value,
    MARKETING_NAME_MAP,
    EFFECT_MAP,
    PRIORITY_MAP
)

logger = logging.getLogger(__name__)

class MarketingService:
    @staticmethod
    async def get_activities_data() -> List[Dict[str, Any]]:
        try:
            query = marketing_activities_table.select()
            results = await database.fetch_all(query)
            
            output = []
            for r in results:
                row = dict(r)
                output.append({
                    "id": row.get("id"),
                    "name": get_mapped_value(MARKETING_NAME_MAP, row.get("name")),
                    "participants": row.get("participants"),
                    "effect": get_mapped_value(EFFECT_MAP, row.get("effect")),
                    "engagement": float(row.get("engagement", 0.0)),
                    "conversion": float(row.get("conversion", 0.0)),
                    "date": row["date"].isoformat() if row.get("date") else None,
                    "priority": get_mapped_value(PRIORITY_MAP, row.get("priority"))
                })
            return output
        except Exception as e:
            logger.error(f"Failed to fetch marketing data: {e}")
            return []