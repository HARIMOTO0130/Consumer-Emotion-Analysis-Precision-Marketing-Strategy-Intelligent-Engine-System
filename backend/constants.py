#-----Attention!!!改前须知----
# 不要修改time项，前端处理时直接在utils/time.js中解析后端的时间戳并转为对应格式
# 具体键值对请看`core/enum_mapping.py`

# 整体统计数据
DEFAULT_STATS = {
    "totalReviews": 24,          # 总评论数
    "positiveCount": 17,          # 正面评论数
    "negativeCount": 7,          # 负面评论数
    "positiveRate": 72.3,          # 正面率(%)
    "trendChange": 3.5,            # 趋势变化(%)
    "alertCount": 2,              # 预警数
    "hotTopicCount": 4,            # 热话题数
    "topTopic": "降温续命就靠这口好火锅"      # 热门话题：new_product(新品发布)
}

# 渠道情感分布
DEFAULT_EMOTION_DISTRIBUTION = [
    # {"channel": "weibo", "positive": 245, "negative": 67, "positivePercent": 78.5},    # weibo(微博)
    {
        "channel": "meituan", 
        "positive": 189, 
        "negative": 45, 
        "positivePercent": 80.7
    },  # meituan(美团h5)
    {
        "channel": "douyin", 
        "positive": 321, 
        "negative": 98, 
        "positivePercent": 76.5
    },  # douyin(抖音)
    {
        "channel": "xiaohongshu", 
        "positive": 245, 
        "negative": 67, 
        "positivePercent": 78.5
    },  # 小红书
]

# 近期评论
DEFAULT_RECENT_COMMENTS = [
    {
        "id": 1,
        "text": "1.空心菜正常，味道偏咸 2.金钱蛋水dangdang的，没有焦香急于出餐 3.辣椒炒肉基本上没动，实在是太咸了，生抽跟盐不要钱似的，吃完后口腔里头仍有咸味一直回味😡 4.那么多就餐人员只有一个服务员，已经很厉害了 午饭期间人多，自助下单后40分钟才开始上菜但出品真的很难吃。 不会再吃了。", 
        "source": 'xiaohongshu', 
        "time": '2025-11-21 13:01:00', 
        "emotion": 'negative'
    },  # source:weibo(微博);emotion:positive(正面)
    {
        "id": 2,
        "text": "物流有点慢，但是产品还不错",
        "source": 'douyin',
        "time": '2025-12-03 19:20:00',
        "emotion": 'neutral'
    },       # source:taobao(淘宝);emotion:neutral(中性)
    {
        "id": 3,
        "text": "抱吃，还不如吃食堂小炒 味道不跟对面小酒馆比，差对面一大截。死咸，色香味一个不占",
        "source": 'meituan',
        "time": '2025-12-10 14:43:00',
        "emotion": 'negative'
    },           # emotion:negative(负面)
    {
        "id": 4,
        "text": "爬完山，小朋友要吃拔丝香蕉，特意过来，但是老板说这个菜太费时间了，所以旺季不做，淡季才有。点了其他的菜，都比较下饭，性价比不错。",
        "source": 'meituan',
        "time": '2025-12-10 15:21:00',
        "emotion": 'positive'
    },     # source:xiaohongshu(小红书);emotion:positive(正面)
    {
        "id": 5,
        "text": "看着平平无奇，实则内有乾坤，光盘",
        "source": 'xiaohongshu',
        "time": '2026-01-12 00:00:00',
        "emotion": 'positive'
    }         # source:tmall(天猫);emotion:negative(负面)
]

# 详细评论
DEFAULT_DETAILED_COMMENTS = [
    {
        "text": "看着平平无奇，实则内有乾坤，光盘",
        "source": 'xiaohongshu',
        "sentiment": 'positive',
        "intensity": 'strong',
        "timestamp": '2025-10-21 10:25:00'
    },  # source:weibo(微博);sentiment:positive(正面);intensity:strong(强)
    {
        "text": "在珠海点到一家好吃的湘菜\n这个小炒牛肉太香了\n干完一整碗饭 撑 ​",
        "source": 'meituan',
        "sentiment": 'positive',
        "intensity": 'medium',
        "timestamp": '2025-11-11 10:22:00'
    },       # source:taobao(淘宝);sentiment:neutral(中性);intensity:medium(中)
    {
        "text": "“菜品新鲜”“味道不错”“经济实惠”“包装严实”#（套餐）紫苏炒牛蛙+五常香米饭+赠品三选一#好吃 分量足 服务态度好，性价比高，推荐👍",
        "source": 'meituan',
        "sentiment": 'negative',
        "intensity": 'strong',
        "timestamp": '2025-12-01 00:00:00'
    },           # source:jd(京东);sentiment:negative(负面);intensity:strong(强)
    {
        "text": "性价比很高，值得推荐",
        "source": 'xiaohongshu',
        "sentiment": 'positive',
        "intensity": 'medium',
        "timestamp": '2025-12-03 00:00:00'
    },     # source:xiaohongshu(小红书);sentiment:positive(正面);intensity:medium(中)
    {
        "text": "牛肉咬不动，味道不好",
        "source": 'meituan',
        "sentiment": 'negative',
        "intensity": 'strong',
        "timestamp": '2025-12-12 00:00:00'
    },         # source:tmall(天猫);sentiment:negative(负面);intensity:strong(强)
    {
        "text": "好吃美味推荐购买便宜优惠",
        "source": 'meituan',
        "sentiment": 'positive',
        "intensity": 'medium',
        "timestamp": '2025-12-21 00:00:00'
    }        # source:pdd(拼多多);sentiment:positive(正面);intensity:medium(中)
]

# 营销活动（participants数值化：2.4万→24000）
DEFAULT_MARKETING_ACTIVITIES = [
    {
        "id": 1,
        "name": '湘遇双 11，食惠全开',
        "participants": 148,
        "effect": 'excellent',
        "engagement": 56,
        "conversion": 12,
        "date": '2025-11-11 00:00:00',
        "priority": 'high'
    },  # name:double11_promotion(双11促销);effect:excellent(优秀);priority:high(高)
    {
        "id": 2, 
        "name": '鲜湘新烹，尝鲜有礼', 
        "participants": 27, 
        "effect": 'good', 
        "engagement": 72, 
        "conversion": 3, 
        "date": '2025-10-15 00:00:00', 
        "priority": 'medium'
    },     # name:new_product_launch(新品上市);effect:good(良好);priority:medium(中)
    {
        "id": 3, 
        "name": '合味湘厨，联名臻享', 
        "participants": 48, 
        "effect": 'average', 
        "engagement": 56, 
        "conversion": 5, 
        "date": '2023-09-20 00:00:00', 
        "priority": 'low'
    }        # name:brand_cooperation(品牌联合);effect:average(一般);priority:low(低)
]

# 洞察信息
DEFAULT_INSIGHTS = [
    {
        "id": 1, 
        "type": 'trend', 
        "date": '2025-12-21 00:00:00', 
        "text": '产品质量相关的正面情感显著增加，可能与最近的质量改进措施有关', 
        "action": 'continue', 
        "actionText": '继续推进'
    },  # type:trend(趋势洞察);actionText:continue(继续推进)
    {
        "id": 2,
        "type": 'risk', 
        "date": '2025-12-27 00:00:00', 
        "text": '物流配送相关的负面情感有所上升，需关注配送服务质量', 
        "action": 'optimize', 
        "actionText": '优化物流'
    },                # type:risk(风险预警);actionText:optimize(优化物流)
    {
        "id": 3, 
        "type": 'opportunity', 
        "date": '2025-12-25 00:00:00', 
        "text": '年轻用户群体对产品的互动功能表现出浓厚兴趣', 
        "action": 'develop', 
        "actionText": '开发功能'
    }        # type:opportunity(机会发现);actionText:develop(开发功能)
]

# 详细洞察
DEFAULT_DETAILED_INSIGHTS = [
    {
        "id": 1, 
        "title": '产品质量持续改善', 
        "description": '最近一个月，关于产品质量的正面评价增加了15%', 
        "recommendation": '继续保持高质量标准，并扩大宣传', 
        "priority": 'high', 
        "expectedOutcome": '品牌名誉提升'
    },  # title:quality_improvement(产品质量持续改善);priority:high(高)
    {
        "id": 2,
        "title": '物流服务待优化', 
        "description": '物流配送相关的投诉在过去两周增加了8%', 
        "recommendation": '与物流合作伙伴协商改进服务标准', 
        "priority": 'medium', 
        "expectedOutcome": '顾客满意度提升'
    },  # title:logistics_optimization(物流服务待优化);priority:medium(中)
    {
        "id": 3, 
        "title": '年轻用户互动需求', 
        "description": '18-30岁用户对社交分享功能的需求明显增长', 
        "recommendation": '开发更多社交互动功能', 
        "priority": 'medium', 
        "expectedOutcome": '用户粘性提升'
    }  # title:young_user_demand(年轻用户互动需求);priority:medium(中)
]

# 趋势洞察
DEFAULT_TREND_INSIGHTS = [
    {
        "id": 1, 
        "text": '近一周正面情感呈稳步上升趋势，主要受益于新产品发布'
    },
    {
        "id": 2,
        "text": '价格敏感度在周末时段明显增加，可能与促销活动有关'
    },
    {
        "id": 3,
        "text": '负面情感主要集中在物流和售后环节，需重点关注'
    },
    {
        "id": 4, 
        "text": '社交媒体上的情感波动较大，需加强监控'
    }
]

# 预警信息
DEFAULT_ALERTS = [
    {
        "id": 1, 
        "title": '物流投诉增加', 
        "type": 'risk', 
        "severity": 'high', 
        "date": '2026-01-21 10:25:00', 
        "status": 'pending'
    },  # title:logistics_complaint_rise(物流投诉增加);severity:high(高);status:pending(待处理)
    {
        "id": 2, 
        "title": '产品质量质疑', 
        "type": 'risk', 
        "severity": 'medium', 
        "date": '2025-12-28 09:45:00', 
        "status": 'processing'
    },  # title:product_quality_doubt(产品质量质疑);severity:medium(中);status:processing(处理中)
    {
        "id": 3, 
        "title": '竞品负面营销', 
        "type": 'risk', 
        "severity": 'low', 
        "date": '2025-11-29 08:30:00', 
        "status": 'completed'
    },  # title:competitor_negative_marketing(竞品负面营销);severity:low(低);status:completed(已处理)
    {
        "id": 4, 
        "title": '服务态度投诉', 
        "type": 'risk', 
        "severity": 'medium', 
        "date": '2026-01-30 17:20:00', 
        "status": 'pending'
    }  # title:service_attitude_complaint(服务态度投诉);severity:medium(中);status:pending(待处理)
]

# 热门话题
DEFAULT_TOPICS = [
    {
        "rank": 1,
        "name": '新品发布',
        "mentions": 24,
        "sentiment": 'positive',
        "trend": 'rising'
    },    # name:new_product(新品发布);sentiment:positive(正面);trend:rising(上升)
    {
        "rank": 2, 
        "name": '价格调整',
        "mentions": 7, 
        "sentiment": 'negative', 
        "trend": 'stable'
    },   # name:price_adjust(价格调整);sentiment:negative(负面);trend:stable(平稳)
    {
        "rank": 3, 
        "name": '售后服务', 
        "mentions": 65, 
        "sentiment": 'neutral', 
        "trend": 'falling'
    },     # name:after_sale(售后服务);sentiment:neutral(中性);trend:falling(下降)
    {
        "rank": 4, 
        "name": '物流配送', 
        "mentions": 4, 
        "sentiment": 'negative', 
        "trend": 'rising'
    },      # name:logistics(物流配送);sentiment:negative(负面);trend:rising(上升)
    {
        "rank": 5, 
        "name": '品牌活动', 
        "mentions": 43, 
        "sentiment": 'positive', 
        "trend": 'stable'
    }  # name:brand_activity(品牌活动);sentiment:positive(正面);trend:stable(平稳)
]