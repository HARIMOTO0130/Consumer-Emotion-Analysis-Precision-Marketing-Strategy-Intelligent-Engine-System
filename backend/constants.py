#-----Attention!!!改前须知----
# 不要修改time项，前端处理时直接在utils/time.js中解析后端的时间戳并转为对应格式
# 具体键值对请看`core/enum_mapping.py`

# 整体统计数据
DEFAULT_STATS = {
    "totalReviews": 1245,          # 总评论数
    "positiveCount": 789,          # 正面评论数
    "negativeCount": 234,          # 负面评论数
    "positiveRate": 72.3,          # 正面率(%)
    "trendChange": 3.5,            # 趋势变化(%)
    "alertCount": 12,              # 预警数
    "hotTopicCount": 8,            # 热话题数
    "topTopic": "new_product"      # 热门话题：new_product(新品发布)
}

# 渠道情感分布
DEFAULT_EMOTION_DISTRIBUTION = [
    {"channel": "weibo", "positive": 245, "negative": 67, "positivePercent": 78.5},    # weibo(微博)
    {"channel": "wechat", "positive": 189, "negative": 45, "positivePercent": 80.7},  # wechat(微信)
    {"channel": "douyin", "positive": 321, "negative": 98, "positivePercent": 76.5},  # douyin(抖音)
    {"channel": "ecommerce", "positive": 156, "negative": 24, "positivePercent": 86.7}# ecommerce(电商)
]

# 近期评论
DEFAULT_RECENT_COMMENTS = [
    {"id": 1, "text": "这款新产品真是太棒了，质量超赞！", "source": 'weibo', "time": '10:25', "emotion": 'positive'},  # source:weibo(微博);emotion:positive(正面)
    {"id": 2, "text": "物流有点慢，但是产品还不错", "source": 'taobao', "time": '10:22', "emotion": 'neutral'},       # source:taobao(淘宝);emotion:neutral(中性)
    {"id": 3, "text": "客服态度很差，不会再买了", "source": 'jd', "time": '10:20', "emotion": 'negative'},           # source:jd(京东);emotion:negative(负面)
    {"id": 4, "text": "性价比很高，值得推荐", "source": 'xiaohongshu', "time": '10:18', "emotion": 'positive'},     # source:xiaohongshu(小红书);emotion:positive(正面)
    {"id": 5, "text": "产品质量有问题，申请退货", "source": 'tmall', "time": '10:15', "emotion": 'negative'}         # source:tmall(天猫);emotion:negative(负面)
]

# 详细评论
DEFAULT_DETAILED_COMMENTS = [
    {"text": "这款新产品真是太棒了，质量超赞！", "source": 'weibo', "sentiment": 'positive', "intensity": 'strong', "timestamp": '2023-12-01 10:25:30'},  # source:weibo(微博);sentiment:positive(正面);intensity:strong(强)
    {"text": "物流有点慢，但是产品还不错", "source": 'taobao', "sentiment": 'neutral', "intensity": 'medium', "timestamp": '2023-12-01 10:22:15'},       # source:taobao(淘宝);sentiment:neutral(中性);intensity:medium(中)
    {"text": "客服态度很差，不会再买了", "source": 'jd', "sentiment": 'negative', "intensity": 'strong', "timestamp": '2023-12-01 10:20:45'},           # source:jd(京东);sentiment:negative(负面);intensity:strong(强)
    {"text": "性价比很高，值得推荐", "source": 'xiaohongshu', "sentiment": 'positive', "intensity": 'medium', "timestamp": '2023-12-01 10:18:20'},     # source:xiaohongshu(小红书);sentiment:positive(正面);intensity:medium(中)
    {"text": "产品质量有问题，申请退货", "source": 'tmall', "sentiment": 'negative', "intensity": 'strong', "timestamp": '2023-12-01 10:15:10'},         # source:tmall(天猫);sentiment:negative(负面);intensity:strong(强)
    {"text": "包装精美，送货很快，非常满意", "source": 'pdd', "sentiment": 'positive', "intensity": 'medium', "timestamp": '2023-12-01 10:12:30'}        # source:pdd(拼多多);sentiment:positive(正面);intensity:medium(中)
]

# 营销活动（participants数值化：2.4万→24000）
DEFAULT_MARKETING_ACTIVITIES = [
    {"id": 1, "name": 'double11_promotion', "participants": 24000, "effect": 'excellent', "engagement": 85, "conversion": 12, "date": '2023-11-11 00:00:00', "priority": 'high'},  # name:double11_promotion(双11促销);effect:excellent(优秀);priority:high(高)
    {"id": 2, "name": 'new_product_launch', "participants": 18000, "effect": 'good', "engagement": 72, "conversion": 8, "date": '2023-10-15 00:00:00', "priority": 'medium'},     # name:new_product_launch(新品上市);effect:good(良好);priority:medium(中)
    {"id": 3, "name": 'brand_cooperation', "participants": 12000, "effect": 'average', "engagement": 56, "conversion": 5, "date": '2023-09-20 00:00:00', "priority": 'low'}        # name:brand_cooperation(品牌联合);effect:average(一般);priority:low(低)
]

# 洞察信息
DEFAULT_INSIGHTS = [
    {"id": 1, "type": 'trend', "date": '2023-12-01 00:00:00', "text": '产品质量相关的正面情感显著增加，可能与最近的质量改进措施有关', "action": 'continue_quality_improvement', "actionText": 'continue'},  # type:trend(趋势洞察);actionText:continue(继续推进)
    {"id": 2, "type": 'risk', "date": '2023-11-27 00:00:00', "text": '物流配送相关的负面情感有所上升，需关注配送服务质量', "action": 'improve_logistics', "actionText": 'optimize'},                # type:risk(风险预警);actionText:optimize(优化物流)
    {"id": 3, "type": 'opportunity', "date": '2023-11-01 00:00:00', "text": '年轻用户群体对产品的互动功能表现出浓厚兴趣', "action": 'develop_engagement_features', "actionText": 'develop'}        # type:opportunity(机会发现);actionText:develop(开发功能)
]

# 详细洞察
DEFAULT_DETAILED_INSIGHTS = [
    {"id": 1, "title": 'quality_improvement', "description": '最近一个月，关于产品质量的正面评价增加了15%', "recommendation": '继续保持高质量标准，并扩大宣传', "priority": 'high', "expectedOutcome": 'brand_reputation提升'},  # title:quality_improvement(产品质量持续改善);priority:high(高)
    {"id": 2, "title": 'logistics_optimization', "description": '物流配送相关的投诉在过去两周增加了8%', "recommendation": '与物流合作伙伴协商改进服务标准', "priority": 'medium', "expectedOutcome": 'customer_satisfaction提升'},  # title:logistics_optimization(物流服务待优化);priority:medium(中)
    {"id": 3, "title": 'young_user_demand', "description": '18-30岁用户对社交分享功能的需求明显增长', "recommendation": '开发更多社交互动功能', "priority": 'medium', "expectedOutcome": 'user_stickiness提升'}  # title:young_user_demand(年轻用户互动需求);priority:medium(中)
]

# 趋势洞察
DEFAULT_TREND_INSIGHTS = [
    {"id": 1, "text": '近一周正面情感呈稳步上升趋势，主要受益于新产品发布'},
    {"id": 2, "text": '价格敏感度在周末时段明显增加，可能与促销活动有关'},
    {"id": 3, "text": '负面情感主要集中在物流和售后环节，需重点关注'},
    {"id": 4, "text": '社交媒体上的情感波动较大，需加强监控'}
]

# 预警信息
DEFAULT_ALERTS = [
    {"id": 1, "title": 'logistics_complaint_rise', "type": 'risk', "severity": 'high', "date": '2023-12-01 10:25:00', "status": 'pending'},  # title:logistics_complaint_rise(物流投诉增加);severity:high(高);status:pending(待处理)
    {"id": 2, "title": 'product_quality_doubt', "type": 'risk', "severity": 'medium', "date": '2023-12-01 09:45:00', "status": 'processing'},  # title:product_quality_doubt(产品质量质疑);severity:medium(中);status:processing(处理中)
    {"id": 3, "title": 'competitor_negative_marketing', "type": 'risk', "severity": 'low', "date": '2023-12-01 08:30:00', "status": 'completed'},  # title:competitor_negative_marketing(竞品负面营销);severity:low(低);status:completed(已处理)
    {"id": 4, "title": 'service_attitude_complaint', "type": 'risk', "severity": 'medium', "date": '2023-11-30 17:20:00', "status": 'pending'}  # title:service_attitude_complaint(服务态度投诉);severity:medium(中);status:pending(待处理)
]

# 热门话题
DEFAULT_TOPICS = [
    {"rank": 1, "name": 'new_product', "mentions": 1245, "sentiment": 'positive', "trend": 'rising'},    # name:new_product(新品发布);sentiment:positive(正面);trend:rising(上升)
    {"rank": 2, "name": 'price_adjust', "mentions": 987, "sentiment": 'negative', "trend": 'stable'},   # name:price_adjust(价格调整);sentiment:negative(负面);trend:stable(平稳)
    {"rank": 3, "name": 'after_sale', "mentions": 765, "sentiment": 'neutral', "trend": 'falling'},     # name:after_sale(售后服务);sentiment:neutral(中性);trend:falling(下降)
    {"rank": 4, "name": 'logistics', "mentions": 654, "sentiment": 'negative', "trend": 'rising'},      # name:logistics(物流配送);sentiment:negative(负面);trend:rising(上升)
    {"rank": 5, "name": 'brand_activity', "mentions": 543, "sentiment": 'positive', "trend": 'stable'}  # name:brand_activity(品牌活动);sentiment:positive(正面);trend:stable(平稳)
]