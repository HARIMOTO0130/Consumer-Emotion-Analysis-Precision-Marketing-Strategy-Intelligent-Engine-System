/**
 * @desc: 数据库枚举类型映射
 * @author: js
 * @version:2026-01-28
 * @see：26-01-28:创建文档 
 */

export const CHANNEL_MAP = {
  'weibo': '微博',
  'wechat': '微信',
  'douyin': '抖音',
  'taobao': '淘宝',
  'jd': '京东',
  'tmall': '天猫',
  'xiaohongshu': '小红书',
  'pdd': '拼多多',
  'ecommerce': '电商平台'
};

export const EMOTION_MAP = {
  'positive': '正面',
  'negative': '负面',
  'neutral': '中性'
};

export const INTENSITY_MAP = {
  'strong': '强烈',
  'medium': '中等',
  'weak': '轻微'
};

export const INSIGHT_TYPE_MAP = {
  'trend': '趋势洞察',
  'risk': '风险预警',
  'opportunity': '机会分析'
};

export const PRIORITY_MAP = {
  'high': '高',
  'medium': '中',
  'low': '低'
};

export const ACTION_TEXT_MAP = {
  'optimize': '继续推进',
  'improve': '优化包装',
  'promote': '开发功能',
  'maintain': '保持现状',
  'adjust': '调整策略'
};

export const MARKETING_NAME_MAP = {
  'double11_promotion': '双11促销活动',
  'new_product_launch': '新品上市推广',
  'brand_cooperation': '品牌联合营销',
  'seasonal_promotion': '季节性促销',
  'member_exclusive': '会员专属活动'
};

export const EFFECT_MAP = {
  'excellent': '优秀',
  'good': '良好',
  'average': '一般',
  'poor': '较差'
};

export const TOPIC_NAME_MAP = {
  'new_product': '新品发布',
  'price_adjust': '价格调整',
  'after_sale': '售后服务',
  'logistics': '物流配送',
  'brand_activity': '品牌活动'
};

export const TREND_MAP = {
  'rising': '上升',
  'stable': '平稳',
  'falling': '下降'
};

export const ALERT_STATUS_MAP = {
  'pending': '待处理',
  'processing': '处理中',
  'completed': '已完成'
};

export const ACTION_TYPE = {
  'trend': "趋势洞察",
  "risk": "风险预警",
  "opportunity":"机会发现"
}

/**
 * 通用枚举值映射函数
 * @param {Object} map - 映射表
 * @param {string} key - 要映射的键
 * @param {string} defaultValue - 默认值（可选）
 * @returns {string} 映射后的值
 */
export function getMappedValue(map, key, defaultValue = '') {
  if (!map || typeof map !== 'object') {
    console.warn('无效的映射表:', map);
    return defaultValue;
  }
  return map[key] || defaultValue;
}

// 快捷方法：渠道映射
export function getChannelName(key, defaultValue = '') {
  return getMappedValue(CHANNEL_MAP, key, defaultValue);
}

// 快捷方法：情感映射
export function getEmotionName(key, defaultValue = '') {
  return getMappedValue(EMOTION_MAP, key, defaultValue);
}

// 快捷方法：强度映射
export function getIntensityName(key, defaultValue = '') {
  return getMappedValue(INTENSITY_MAP, key, defaultValue);
}

// 快捷方法：洞察类型映射
export function getInsightTypeName(key, defaultValue = '') {
  return getMappedValue(INSIGHT_TYPE_MAP, key, defaultValue);
}

// 快捷方法：优先级映射
export function getPriorityName(key, defaultValue = '') {
  return getMappedValue(PRIORITY_MAP, key, defaultValue);
}

// 快捷方法：营销活动名称映射
export function getMarketingName(key, defaultValue = '') {
  return getMappedValue(MARKETING_NAME_MAP, key, defaultValue);
}

// 快捷方法：效果映射
export function getEffectName(key, defaultValue = '') {
  return getMappedValue(EFFECT_MAP, key, defaultValue);
}

// 快捷方法：话题名称映射
export function getTopicName(key, defaultValue = '') {
  return getMappedValue(TOPIC_NAME_MAP, key, defaultValue);
}

// 快捷方法：趋势映射
export function getTrendName(key, defaultValue = '') {
  return getMappedValue(TREND_MAP, key, defaultValue);
}

// 快捷方法：预警状态映射
export function getAlertStatusName(key, defaultValue = '') {
  return getMappedValue(ALERT_STATUS_MAP, key, defaultValue);
}
export function getActionTypeName(key, defaultValue = '') {
  return getMappedValue(ACTION_TYPE, key, defaultValue);
}