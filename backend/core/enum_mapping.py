# 已废弃，直接修改前端的对应文件
# --------Attention!!!!注意注意--------
# author: jh
# 更新时间：2026-01-28
# 更新内容：
#   26-01-28:创建文档

# 为了扩展性没有直接在MySQL中定义ENUM类型，而是使用VARCHAR进行存储，修改下表时注意
# 1.查询对应同目录下mysql.sql文件的更新日期
# 2.查询需要修改的VARCHAR长度
# 3.更新下表
# 4.更新前端的对应常量（目前还没有）

# 渠道映射 (source/channel)
CHANNEL_MAP = {
    "weibo": "微博",
    "wechat": "微信",
    "douyin": "抖音",
    "ecommerce": "电商",
    "taobao": "淘宝",
    "jd": "京东",
    "tmall": "天猫",
    "xiaohongshu": "小红书",
    "pdd": "拼多多"
}

# 情感映射 (emotion/sentiment)
EMOTION_MAP = {
    "positive": "正面",
    "neutral": "中性",
    "negative": "负面"
}

# 情感强度映射 (intensity)
INTENSITY_MAP = {
    "strong": "强",
    "medium": "中",
    "weak": "弱",
    "强": "强",
    "中": "中",
    "弱": "弱"
}

# 优先级映射 (priority/severity)
PRIORITY_MAP = {
    "high": "高",
    "medium": "中",
    "low": "低"
}

# 营销活动效果映射 (effect)
EFFECT_MAP = {
    "excellent": "优秀",
    "good": "良好",
    "average": "一般"
}

# 预警状态映射 (status)
ALERT_STATUS_MAP = {
    "pending": "待处理",
    "processing": "处理中",
    "completed": "已处理"
}

# 趋势映射 (trend)
TREND_MAP = {
    "rising": "上升",
    "stable": "平稳",
    "falling": "下降"
}

# 洞察类型映射 (type)
INSIGHT_TYPE_MAP = {
    "trend": "趋势洞察",
    "risk": "风险预警",
    "opportunity": "机会发现"
}

# 热门话题名称映射 (name)
TOPIC_NAME_MAP = {
    "new_product": "新品发布",
    "price_adjust": "价格调整",
    "after_sale": "售后服务",
    "logistics": "物流配送",
    "brand_activity": "品牌活动"
}

# 营销活动名称映射 (name)
MARKETING_NAME_MAP = {
    "double11_promotion": "双11促销活动",
    "new_product_launch": "新品上市推广",
    "brand_cooperation": "品牌联合营销"
}

# 洞察行动文本映射 (action_text)
ACTION_TEXT_MAP = {
    "continue": "继续推进",
    "optimize": "优化物流",
    "develop": "开发功能"
}

# 热门话题TOP映射 (top_topic)
TOP_TOPIC_MAP = {
    "new_product": "新品发布"
}

# 通用映射函数
def get_mapped_value(mapping_dict: dict, key: str, default=None):
    if not key:
        return default or key
    return mapping_dict.get(key.strip(), default or key)