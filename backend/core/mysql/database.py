import os
import logging
import databases
import sqlalchemy
from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.base import metadata
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4") 

# 构建数据库连接 URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"

# 初始化数据库连接
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 检查连接是否有效
    pool_size=10,        # 连接池大小
    max_overflow=20,     # 最大溢出连接数
    pool_recycle=3600    # 连接回收时间（1小时）
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
    except Exception as e:
        logger.error(f"检查表数据失败: {e}")
        return False

async def insert_mock_data():
    """初始化 Mock 数据(ENABLE_DATABASE_MOCKS)"""
    enable_mocks = os.getenv("ENABLE_DATABASE_MOCKS", "True").strip().lower()
    INIT_MOCK = enable_mocks in ["true", "1", "yes", "on"]
    
    if not INIT_MOCK:
        logger.info("Mock 数据插入已禁用（ENABLE_DATABASE_MOCKS=False）")
        return

    logger.info("开始插入 Mock 数据...")
    
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
            top_topic=DEFAULT_STATS["topTopic"],
            updated_at=sqlalchemy.func.now()
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
                emotion="positive" if item.get("sentiment") in ["正面", "positive"] else 
                        "negative" if item.get("sentiment") in ["负面", "negative"] else "neutral",
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
                    sentiment="正面" if item["emotion"] == "positive" else 
                              "负面" if item["emotion"] == "negative" else "中性",
                    intensity="中",
                    timestamp=f"2023-12-01 {item['time']}:00"
                ))

    # Marketing
    if not row_exists(marketing_activities_table):
        logger.info("Inserting mock marketing activities...")
        for item in DEFAULT_MARKETING_ACTIVITIES:
            participants = item["participants"]
            if isinstance(participants, str):
                if "万" in participants:
                    participants = int(float(participants.replace("万", "")) * 10000)
                elif "千" in participants:
                    participants = int(float(participants.replace("千", "")) * 1000)
                else:
                    participants = int(participants)
            
            await database.execute(marketing_activities_table.insert().values(
                name=item["name"],
                participants=participants,
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
    
    logger.info("Mock 数据插入完成")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Lifespan starting: Creating tables...")
    metadata.create_all(engine)

    await database.connect()
    logger.info(f"Connected to MySQL database: {DB_NAME}")
    
    await insert_mock_data()

    yield

    await database.disconnect()
    logger.info("Disconnected from MySQL database.")

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