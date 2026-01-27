import time
import random
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import databases
import sqlalchemy
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./emotion_analysis.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# 数据库表定义
stats_table = sqlalchemy.Table(
    "stats",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("total_reviews", sqlalchemy.Integer),
    sqlalchemy.Column("positive_count", sqlalchemy.Integer),
    sqlalchemy.Column("negative_count", sqlalchemy.Integer),
    sqlalchemy.Column("positive_rate", sqlalchemy.Float),
    sqlalchemy.Column("trend_change", sqlalchemy.Float),
    sqlalchemy.Column("alert_count", sqlalchemy.Integer),
    sqlalchemy.Column("hot_topic_count", sqlalchemy.Integer),
    sqlalchemy.Column("top_topic", sqlalchemy.String),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime),
)

emotion_distribution_table = sqlalchemy.Table(
    "emotion_distribution",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("channel", sqlalchemy.String),
    sqlalchemy.Column("positive", sqlalchemy.Integer),
    sqlalchemy.Column("negative", sqlalchemy.Integer),
    sqlalchemy.Column("positive_percent", sqlalchemy.Float),
)

comments_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("source", sqlalchemy.String),
    sqlalchemy.Column("time", sqlalchemy.String),
    sqlalchemy.Column("emotion", sqlalchemy.String),
    sqlalchemy.Column("sentiment", sqlalchemy.String),
    sqlalchemy.Column("intensity", sqlalchemy.String),
    sqlalchemy.Column("timestamp", sqlalchemy.String),
)

marketing_activities_table = sqlalchemy.Table(
    "marketing_activities",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("participants", sqlalchemy.String),
    sqlalchemy.Column("effect", sqlalchemy.String),
    sqlalchemy.Column("engagement", sqlalchemy.Float),
    sqlalchemy.Column("conversion", sqlalchemy.Float),
    sqlalchemy.Column("date", sqlalchemy.String),
    sqlalchemy.Column("priority", sqlalchemy.String),
)

insights_table = sqlalchemy.Table(
    "insights",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("type", sqlalchemy.String),
    sqlalchemy.Column("date", sqlalchemy.String),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("action", sqlalchemy.String),
    sqlalchemy.Column("action_text", sqlalchemy.String),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("recommendation", sqlalchemy.String),
    sqlalchemy.Column("priority", sqlalchemy.String),
    sqlalchemy.Column("expected_outcome", sqlalchemy.String),
)

trend_insights_table = sqlalchemy.Table(
    "trend_insights",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
)

alerts_table = sqlalchemy.Table(
    "alerts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("type", sqlalchemy.String),
    sqlalchemy.Column("severity", sqlalchemy.String),
    sqlalchemy.Column("date", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.String),
)

topics_table = sqlalchemy.Table(
    "topics",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("rank", sqlalchemy.Integer),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("mentions", sqlalchemy.Integer),
    sqlalchemy.Column("sentiment", sqlalchemy.String),
    sqlalchemy.Column("trend", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI(title="Consumer Emotion Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 预设数据
DEFAULT_STATS = {
    "totalReviews": 1245,
    "positiveCount": 789,
    "negativeCount": 234,
    "positiveRate": 72.3,
    "trendChange": 3.5,
    "alertCount": 12,
    "hotTopicCount": 8,
    "topTopic": "新品发布"
}

DEFAULT_EMOTION_DISTRIBUTION = [
    {"channel": "微博", "positive": 245, "negative": 67, "positivePercent": 78.5},
    {"channel": "微信", "positive": 189, "negative": 45, "positivePercent": 80.7},
    {"channel": "抖音", "positive": 321, "negative": 98, "positivePercent": 76.5},
    {"channel": "电商", "positive": 156, "negative": 24, "positivePercent": 86.7}
]

DEFAULT_RECENT_COMMENTS = [
    {"id": 1, "text": "这款新产品真是太棒了，质量超赞！", "source": '微博', "time": '10:25', "emotion": 'positive'},
    {"id": 2, "text": "物流有点慢，但是产品还不错", "source": '淘宝', "time": '10:22', "emotion": 'neutral'},
    {"id": 3, "text": "客服态度很差，不会再买了", "source": '京东', "time": '10:20', "emotion": 'negative'},
    {"id": 4, "text": "性价比很高，值得推荐", "source": '小红书', "time": '10:18', "emotion": 'positive'},
    {"id": 5, "text": "产品质量有问题，申请退货", "source": '天猫', "time": '10:15', "emotion": 'negative'}
]

DEFAULT_DETAILED_COMMENTS = [
    {"text": "这款新产品真是太棒了，质量超赞！", "source": '微博', "sentiment": '正面', "intensity": '强', "timestamp": '2023-12-01 10:25:30'},
    {"text": "物流有点慢，但是产品还不错", "source": '淘宝', "sentiment": '中性', "intensity": '中', "timestamp": '2023-12-01 10:22:15'},
    {"text": "客服态度很差，不会再买了", "source": '京东', "sentiment": '负面', "intensity": '强', "timestamp": '2023-12-01 10:20:45'},
    {"text": "性价比很高，值得推荐", "source": '小红书', "sentiment": '正面', "intensity": '中', "timestamp": '2023-12-01 10:18:20'},
    {"text": "产品质量有问题，申请退货", "source": '天猫', "sentiment": '负面', "intensity": '强', "timestamp": '2023-12-01 10:15:10'},
    {"text": "包装精美，送货很快，非常满意", "source": '拼多多', "sentiment": '正面', "intensity": '中', "timestamp": '2023-12-01 10:12:30'}
]

DEFAULT_MARKETING_ACTIVITIES = [
    {"id": 1, "name": '双11促销活动', "participants": '2.4万', "effect": '优秀', "engagement": 85, "conversion": 12, "date": '2023-11-11', "priority": 'high'},
    {"id": 2, "name": '新品上市推广', "participants": '1.8万', "effect": '良好', "engagement": 72, "conversion": 8, "date": '2023-10-15', "priority": 'medium'},
    {"id": 3, "name": '品牌联合营销', "participants": '1.2万', "effect": '一般', "engagement": 56, "conversion": 5, "date": '2023-09-20', "priority": 'low'}
]

DEFAULT_INSIGHTS = [
    {"id": 1, "type": '趋势洞察', "date": '今日', "text": '产品质量相关的正面情感显著增加，可能与最近的质量改进措施有关', "action": 'continue_quality_improvement', "actionText": '继续推进'},
    {"id": 2, "type": '风险预警', "date": '本周', "text": '物流配送相关的负面情感有所上升，需关注配送服务质量', "action": 'improve_logistics', "actionText": '优化物流'},
    {"id": 3, "type": '机会发现', "date": '本月', "text": '年轻用户群体对产品的互动功能表现出浓厚兴趣', "action": 'develop_engagement_features', "actionText": '开发功能'}
]

DEFAULT_DETAILED_INSIGHTS = [
    {"id": 1, "title": '产品质量持续改善', "description": '最近一个月，关于产品质量的正面评价增加了15%', "recommendation": '继续保持高质量标准，并扩大宣传', "priority": '高', "expectedOutcome": '进一步提升品牌声誉'},
    {"id": 2, "title": '物流服务待优化', "description": '物流配送相关的投诉在过去两周增加了8%', "recommendation": '与物流合作伙伴协商改进服务标准', "priority": '中', "expectedOutcome": '减少负面评价，提高客户满意度'},
    {"id": 3, "title": '年轻用户互动需求', "description": '18-30岁用户对社交分享功能的需求明显增长', "recommendation": '开发更多社交互动功能', "priority": '中', "expectedOutcome": '提高用户粘性和活跃度'}
]

DEFAULT_TREND_INSIGHTS = [
    {"id": 1, "text": '近一周正面情感呈稳步上升趋势，主要受益于新产品发布'},
    {"id": 2, "text": '价格敏感度在周末时段明显增加，可能与促销活动有关'},
    {"id": 3, "text": '负面情感主要集中在物流和售后环节，需重点关注'},
    {"id": 4, "text": '社交媒体上的情感波动较大，需加强监控'}
]

DEFAULT_ALERTS = [
    {"id": 1, "title": '物流投诉增加', "type": '风险', "severity": '高', "date": '2023-12-01 10:25', "status": '待处理'},
    {"id": 2, "title": '产品质量质疑', "type": '风险', "severity": '中', "date": '2023-12-01 09:45', "status": '处理中'},
    {"id": 3, "title": '竞品负面营销', "type": '风险', "severity": '低', "date": '2023-12-01 08:30', "status": '已处理'},
    {"id": 4, "title": '服务态度投诉', "type": '风险', "severity": '中', "date": '2023-11-30 17:20', "status": '待处理'}
]

DEFAULT_TOPICS = [
    {"rank": 1, "name": '新品发布', "mentions": 1245, "sentiment": '正面', "trend": '上升'},
    {"rank": 2, "name": '价格调整', "mentions": 987, "sentiment": '负面', "trend": '平稳'},
    {"rank": 3, "name": '售后服务', "mentions": 765, "sentiment": '中性', "trend": '下降'},
    {"rank": 4, "name": '物流配送', "mentions": 654, "sentiment": '负面', "trend": '上升'},
    {"rank": 5, "name": '品牌活动', "mentions": 543, "sentiment": '正面', "trend": '平稳'}
]

class StatsService:
    async def get_stats_data(self, time_range: str) -> Dict[str, Any]:
        try:
            query = stats_table.select().where(
                stats_table.c.updated_at >= datetime.now() - timedelta(days=30)
            ).order_by(stats_table.c.updated_at.desc()).limit(1)
            result = await database.fetch_one(query)
            
            if result:
                return {
                    "totalReviews": result["total_reviews"],
                    "positiveCount": result["positive_count"],
                    "negativeCount": result["negative_count"],
                    "positiveRate": result["positive_rate"],
                    "trendChange": result["trend_change"],
                    "alertCount": result["alert_count"],
                    "hotTopicCount": result["hot_topic_count"],
                    "topTopic": result["top_topic"]
                }
            return DEFAULT_STATS
        except Exception:
            return DEFAULT_STATS

class EmotionDistributionService:
    async def get_distribution_data(self) -> List[Dict[str, Any]]:
        try:
            query = emotion_distribution_table.select()
            results = await database.fetch_all(query)
            
            if results:
                return [
                    {
                        "channel": r["channel"],
                        "positive": r["positive"],
                        "negative": r["negative"],
                        "positivePercent": r["positive_percent"]
                    }
                    for r in results
                ]
            return DEFAULT_EMOTION_DISTRIBUTION
        except Exception:
            return DEFAULT_EMOTION_DISTRIBUTION

class CommentsService:
    async def get_recent_comments(self, limit: int = 5) -> List[Dict[str, Any]]:
        try:
            query = comments_table.select().order_by(comments_table.c.id.desc()).limit(limit)
            results = await database.fetch_all(query)
            
            if results:
                return [
                    {
                        "id": r["id"],
                        "text": r["text"],
                        "source": r["source"],
                        "time": r["time"],
                        "emotion": r["emotion"]
                    }
                    for r in results
                ]
            return DEFAULT_RECENT_COMMENTS
        except Exception:
            return DEFAULT_RECENT_COMMENTS
    
    async def get_detailed_comments(self) -> List[Dict[str, Any]]:
        try:
            query = comments_table.select().order_by(comments_table.c.id.desc()).limit(10)
            results = await database.fetch_all(query)
            
            if results:
                return [
                    {
                        "text": r["text"],
                        "source": r["source"],
                        "sentiment": r["sentiment"],
                        "intensity": r["intensity"],
                        "timestamp": r["timestamp"]
                    }
                    for r in results
                ]
            return DEFAULT_DETAILED_COMMENTS
        except Exception:
            return DEFAULT_DETAILED_COMMENTS

class MarketingService:
    async def get_activities_data(self) -> List[Dict[str, Any]]:
        try:
            query = marketing_activities_table.select()
            results = await database.fetch_all(query)
            
            if results:
                return [
                    {
                        "id": r["id"],
                        "name": r["name"],
                        "participants": r["participants"],
                        "effect": r["effect"],
                        "engagement": r["engagement"],
                        "conversion": r["conversion"],
                        "date": r["date"],
                        "priority": r["priority"]
                    }
                    for r in results
                ]
            return DEFAULT_MARKETING_ACTIVITIES
        except Exception:
            return DEFAULT_MARKETING_ACTIVITIES

class InsightsService:
    async def get_insights_data(self) -> List[Dict[str, Any]]:
        try:
            query = insights_table.select().limit(3)
            results = await database.fetch_all(query)
            
            if results:
                return [
                    {
                        "id": r["id"],
                        "type": r["type"],
                        "date": r["date"],
                        "text": r["text"],
                        "action": r["action"],
                        "actionText": r["action_text"]
                    }
                    for r in results
                ]
            return DEFAULT_INSIGHTS
        except Exception:
            return DEFAULT_INSIGHTS
    
    async def get_detailed_insights(self) -> List[Dict[str, Any]]:
        try:
            query = insights_table.select().limit(3)
            results = await database.fetch_all(query)
            
            if results:
                return [
                    {
                        "id": r["id"],
                        "title": r["title"],
                        "description": r["description"],
                        "recommendation": r["recommendation"],
                        "priority": r["priority"],
                        "expectedOutcome": r["expected_outcome"]
                    }
                    for r in results
                ]
            return DEFAULT_DETAILED_INSIGHTS
        except Exception:
            return DEFAULT_DETAILED_INSIGHTS

class TrendInsightsService:
    async def get_trend_insights(self) -> List[Dict[str, Any]]:
        try:
            query = trend_insights_table.select()
            results = await database.fetch_all(query)
            
            if results:
                return [
                    {
                        "id": r["id"],
                        "text": r["text"]
                    }
                    for r in results
                ]
            return DEFAULT_TREND_INSIGHTS
        except Exception:
            return DEFAULT_TREND_INSIGHTS

class AlertsService:
    async def get_alerts(self) -> List[Dict[str, Any]]:
        try:
            query = alerts_table.select()
            results = await database.fetch_all(query)
            
            if results:
                return [
                    {
                        "id": r["id"],
                        "title": r["title"],
                        "type": r["type"],
                        "severity": r["severity"],
                        "date": r["date"],
                        "status": r["status"]
                    }
                    for r in results
                ]
            return DEFAULT_ALERTS
        except Exception:
            return DEFAULT_ALERTS

class TopicsService:
    async def get_topics(self) -> List[Dict[str, Any]]:
        try:
            query = topics_table.select()
            results = await database.fetch_all(query)
            
            if results:
                return [
                    {
                        "rank": r["rank"],
                        "name": r["name"],
                        "mentions": r["mentions"],
                        "sentiment": r["sentiment"],
                        "trend": r["trend"]
                    }
                    for r in results
                ]
            return DEFAULT_TOPICS
        except Exception:
            return DEFAULT_TOPICS

# 服务实例
stats_service = StatsService()
emotion_distribution_service = EmotionDistributionService()
comments_service = CommentsService()
marketing_service = MarketingService()
insights_service = InsightsService()
trend_insights_service = TrendInsightsService()
alerts_service = AlertsService()
topics_service = TopicsService()

# API路由
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/api/stats")
async def get_stats(time_range: str = Query("24h", description="时间范围")):
    return await stats_service.get_stats_data(time_range)

@app.get("/api/emotion-distribution")
async def get_emotion_distribution():
    return await emotion_distribution_service.get_distribution_data()

@app.get("/api/comments/recent")
async def get_recent_comments(limit: int = Query(5, description="评论数量")):
    return await comments_service.get_recent_comments(limit)

@app.get("/api/comments/detailed")
async def get_detailed_comments():
    return await comments_service.get_detailed_comments()

@app.get("/api/marketing/activities")
async def get_marketing_activities():
    return await marketing_service.get_activities_data()

@app.get("/api/insights")
async def get_insights():
    return await insights_service.get_insights_data()

@app.get("/api/insights/detailed")
async def get_detailed_insights():
    return await insights_service.get_detailed_insights()

@app.get("/api/trend-insights")
async def get_trend_insights():
    return await trend_insights_service.get_trend_insights()

@app.get("/api/alerts")
async def get_alerts():
    return await alerts_service.get_alerts()

@app.get("/api/topics")
async def get_topics():
    return await topics_service.get_topics()

@app.get("/api/batch-data")
async def get_batch_data(time_range: str = Query("24h", description="时间范围")):
    """批量获取所有数据，减少HTTP请求次数"""
    try:
        # 并行执行所有数据获取操作
        stats, emotion_distribution, recent_comments, detailed_comments, marketing_activities, insights, detailed_insights, trend_insights, alerts, topics = await asyncio.gather(
            stats_service.get_stats_data(time_range),
            emotion_distribution_service.get_distribution_data(),
            comments_service.get_recent_comments(),
            comments_service.get_detailed_comments(),
            marketing_service.get_activities_data(),
            insights_service.get_insights_data(),
            insights_service.get_detailed_insights(),
            trend_insights_service.get_trend_insights(),
            alerts_service.get_alerts(),
            topics_service.get_topics()
        )

        return {
            "stats": stats,
            "emotionDistribution": emotion_distribution,
            "recentComments": recent_comments,
            "detailedComments": detailed_comments,
            "marketingActivities": marketing_activities,
            "insights": insights,
            "detailedInsights": detailed_insights,
            "trendInsights": trend_insights,
            "alerts": alerts,
            "topics": topics
        }
    except Exception as e:
        # 如果批量获取失败，返回默认数据
        return {
            "stats": DEFAULT_STATS,
            "emotionDistribution": DEFAULT_EMOTION_DISTRIBUTION,
            "recentComments": DEFAULT_RECENT_COMMENTS,
            "detailedComments": DEFAULT_DETAILED_COMMENTS,
            "marketingActivities": DEFAULT_MARKETING_ACTIVITIES,
            "insights": DEFAULT_INSIGHTS,
            "detailedInsights": DEFAULT_DETAILED_INSIGHTS,
            "trendInsights": DEFAULT_TREND_INSIGHTS,
            "alerts": DEFAULT_ALERTS,
            "topics": DEFAULT_TOPICS
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
