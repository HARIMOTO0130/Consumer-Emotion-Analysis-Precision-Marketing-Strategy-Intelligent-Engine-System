# 至2026-01-28，废弃功能
import os
import logging
import databases
import sqlalchemy
from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.base import metadata

logger = logging.getLogger(__name__)

# 数据库配置
DATABASE_URL = "sqlite:///./db/emotion_analysis.db"
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 导入所有模型表
from modules.stats.models import stats_table
from modules.emotion_distribution.models import emotion_distribution_table
from modules.comments.models import comments_table
from modules.marketing.models import marketing_activities_table
from modules.insights.models import insights_table
from modules.trend_insights.models import trend_insights_table
from modules.alerts.models import alerts_table
from modules.topics.models import topics_table

def row_exists(table):
    """检查表中是否存在数据"""
    try:
        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.select(table).limit(1))
            return result.fetchone() is not None
    except Exception:
        return False

async def insert_mock_data():
    """初始化 Mock 数据"""
    from constants import (
        DEFAULT_STATS,
        DEFAULT_EMOTION_DISTRIBUTION,
        DEFAULT_RECENT_COMMENTS,
        DEFAULT_MARKETING_ACTIVITIES,
        DEFAULT_INSIGHTS,
        DEFAULT_TREND_INSIGHTS,
        DEFAULT_ALERTS,
        DEFAULT_TOPICS,
        DEFAULT_DETAILED_INSIGHTS,
        DEFAULT_DETAILED_COMMENTS
    )
    
    INIT_MOCK = True
    if not INIT_MOCK:
        logger.info("Mock data initialization skipped")
        return

    db_path = DATABASE_URL.replace("sqlite:///", "")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    detailed_comment_map = {
        (item["text"], item["source"]): item
        for item in DEFAULT_DETAILED_COMMENTS
    }
    insights_detail_map = {
        item["id"]: item for item in DEFAULT_DETAILED_INSIGHTS
    }

    # Stats
    if not row_exists(stats_table):
        logger.info("Inserting mock stats...")
        await database.execute(stats_table.insert().values(
            total_reviews=DEFAULT_STATS["totalReviews"],
            positive_count=DEFAULT_STATS["positiveCount"],
            negative_count=DEFAULT_STATS["negativeCount"],
            positive_rate=DEFAULT_STATS["positiveRate"],
            trend_change=DEFAULT_STATS["trendChange"],
            alert_count=DEFAULT_STATS["alertCount"],
            hot_topic_count=DEFAULT_STATS["hotTopicCount"],
            top_topic=DEFAULT_STATS["topTopic"]
        ))

    # Emotion Distribution
    if not row_exists(emotion_distribution_table):
        logger.info("Inserting mock emotion distribution...")
        for item in DEFAULT_EMOTION_DISTRIBUTION:
            await database.execute(emotion_distribution_table.insert().values(
                channel=item["channel"],
                positive=item["positive"],
                negative=item["negative"],
                positive_percent=item["positivePercent"]
            ))

    # Comments
    if not row_exists(comments_table):
            logger.info("Inserting mock comments...")
            detailed_comment_map = {
                    item["text"]: item for item in DEFAULT_DETAILED_COMMENTS
                }
            for item in DEFAULT_DETAILED_COMMENTS:
                await database.execute(comments_table.insert().values(
                    text=item.get("text"),
                    source=item.get("source"),
                    time=item.get("timestamp", "10:00")[-5:],
                    emotion="positive" if "正面" in item.get("sentiment", "") else "negative",
                    sentiment=item.get("sentiment"),
                    intensity=item.get("intensity"),
                    timestamp=item.get("timestamp")
                ))
        
            for item in DEFAULT_RECENT_COMMENTS:
                if item["text"] not in detailed_comment_map:
                    await database.execute(comments_table.insert().values(
                        text=item["text"],
                        source=item["source"],
                        time=item["time"],
                        emotion=item["emotion"],
                        sentiment="正面" if item["emotion"] == "positive" else "负面",
                        intensity="中",
                        timestamp=f"2023-12-01 {item['time']}:00"
                    ))

    # Marketing
    if not row_exists(marketing_activities_table):
        logger.info("Inserting mock marketing activities...")
        for item in DEFAULT_MARKETING_ACTIVITIES:
            await database.execute(marketing_activities_table.insert().values(
                name=item["name"],
                participants=item["participants"],
                effect=item["effect"],
                engagement=float(item["engagement"]),
                conversion=float(item["conversion"]),
                date=item["date"],
                priority=item["priority"]
            ))

    # Insights
    if not row_exists(insights_table):
        logger.info("Inserting mock insights...")
        for item in DEFAULT_INSIGHTS:
            detail = insights_detail_map.get(item["id"], {})
            await database.execute(insights_table.insert().values(
                type=item["type"],
                date=item["date"],
                text=item["text"],
                action=item["action"],
                action_text=item["actionText"],
                title=detail.get("title"),
                description=detail.get("description"),
                recommendation=detail.get("recommendation"),
                priority=detail.get("priority"),
                expected_outcome=detail.get("expectedOutcome")
            ))

    # Trend Insights
    if not row_exists(trend_insights_table):
        logger.info("Inserting mock trend insights...")
        for item in DEFAULT_TREND_INSIGHTS:
            await database.execute(trend_insights_table.insert().values(text=item["text"]))

    # Alerts
    if not row_exists(alerts_table):
        logger.info("Inserting mock alerts...")
        for item in DEFAULT_ALERTS:
            await database.execute(alerts_table.insert().values(
                title=item["title"],
                type=item["type"],
                severity=item["severity"],
                date=item["date"],
                status=item["status"]
            ))

    # Topics
    if not row_exists(topics_table):
        logger.info("Inserting mock topics...")
        for item in DEFAULT_TOPICS:
            await database.execute(topics_table.insert().values(
                rank=item["rank"],
                name=item["name"],
                mentions=item["mentions"],
                sentiment=item["sentiment"],
                trend=item["trend"]
            ))

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Lifespan starting: Creating tables...")
    metadata.create_all(engine)

    await database.connect()
    logger.info("Database connected. Initializing mock data...")
    await insert_mock_data()

    yield

    await database.disconnect()
    logger.info("Database disconnected.")

def init_app():
    from fastapi.middleware.cors import CORSMiddleware
    app = FastAPI(
        title="Consumer Emotion Analysis API",
        lifespan=lifespan
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app