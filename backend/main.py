import asyncio
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入修改后的数据库初始化函数
from core.database import init_app

app = init_app()

# 设置路由前缀
URL_PREFIX = "/v1/api"

# 导入路由
from modules.stats import router as stats_router
from modules.emotion_distribution import router as emotion_router
from modules.comments import router as comments_router
from modules.marketing import router as marketing_router
from modules.insights import router as insights_router
from modules.trend_insights import router as trend_router
from modules.alerts import router as alerts_router
from modules.topics import router as topics_router

# 注册路由
app.include_router(stats_router, prefix=URL_PREFIX)
app.include_router(emotion_router, prefix=URL_PREFIX)
app.include_router(comments_router, prefix=URL_PREFIX)
app.include_router(marketing_router, prefix=URL_PREFIX)
app.include_router(insights_router, prefix=URL_PREFIX)
app.include_router(trend_router, prefix=URL_PREFIX)
app.include_router(alerts_router, prefix=URL_PREFIX)
app.include_router(topics_router, prefix=URL_PREFIX)


@app.get(URL_PREFIX + "/batch-data")
async def get_batch_data():
    from modules.stats.services import StatsService
    from modules.emotion_distribution.services import EmotionDistributionService
    from modules.comments.services import CommentsService
    from modules.marketing.services import MarketingService
    from modules.insights.services import InsightsService
    from modules.trend_insights.services import TrendInsightsService
    from modules.alerts.services import AlertsService
    from modules.topics.services import TopicsService

    results = await asyncio.gather(
        StatsService.get_stats_data(),
        EmotionDistributionService.get_distribution_data(),
        CommentsService.get_recent_comments(),
        CommentsService.get_detailed_comments(),
        MarketingService.get_activities_data(),
        InsightsService.get_detailed_insights(),
        InsightsService.get_detailed_insights(),
        TrendInsightsService.get_trend_insights(),
        AlertsService.get_alerts(),
        TopicsService.get_topics(),
    )

    (
        stats, emotion, recent, detailed, marketing,
        insights, detailed_insights, trend, alerts, topics
    ) = results

    return {
        "stats": stats,
        "emotionDistribution": emotion,
        "recentComments": recent,
        "detailedComments": detailed,
        "marketingActivities": marketing,
        "insights": insights,
        "detailedInsights": detailed_insights,
        "trendInsights": trend,
        "alerts": alerts,
        "topics": topics,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)