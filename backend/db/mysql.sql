DROP DATABASE IF EXISTS emotion_analysis;
CREATE DATABASE emotion_analysis DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE emotion_analysis;

-- 预警表
DROP TABLE IF EXISTS `alerts`;
CREATE TABLE `alerts` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `title` VARCHAR(255) DEFAULT NULL COMMENT '预警标题（英文：logistics_complaint_rise=物流投诉增加）',
  `type` VARCHAR(50) DEFAULT NULL COMMENT '预警类型（英文：risk=风险）',
  `severity` VARCHAR(20) DEFAULT NULL COMMENT '严重程度（英文：high=高/medium=中/low=低）',
  `date` TIMESTAMP NOT NULL COMMENT '预警时间',
  `status` VARCHAR(20) DEFAULT NULL COMMENT '处理状态（英文：pending=待处理/processing=处理中/completed=已处理）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='预警信息表';

-- 评论表
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `text` TEXT DEFAULT NULL COMMENT '评论内容',
  `source` VARCHAR(50) DEFAULT NULL COMMENT '评论来源（英文：weibo=微博/taobao=淘宝/jd=京东等）',
  `time` VARCHAR(10) DEFAULT NULL COMMENT '评论时分（简化时间）',
  `emotion` VARCHAR(20) DEFAULT NULL COMMENT '情感标签（英文：positive=正面/neutral=中性/negative=负面）',
  `sentiment` VARCHAR(20) DEFAULT NULL COMMENT '情感倾向（英文：positive=正面/neutral=中性/negative=负面）',
  `intensity` VARCHAR(10) DEFAULT NULL COMMENT '情感强度（英文：strong=强/medium=中/weak=弱）',
  `timestamp` TIMESTAMP NOT NULL COMMENT '评论完整时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户评论表';

-- 渠道情感分布表
DROP TABLE IF EXISTS `emotion_distribution`;
CREATE TABLE `emotion_distribution` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `channel` VARCHAR(50) DEFAULT NULL COMMENT '渠道（英文：weibo=微博/wechat=微信/douyin=抖音/ecommerce=电商）',
  `positive` INT DEFAULT NULL COMMENT '正面评论数',
  `negative` INT DEFAULT NULL COMMENT '负面评论数',
  `positive_percent` FLOAT DEFAULT NULL COMMENT '正面率(%)',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='渠道情感分布表';

-- 洞察信息表
DROP TABLE IF EXISTS `insights`;
CREATE TABLE `insights` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `type` VARCHAR(50) DEFAULT NULL COMMENT '洞察类型（英文：trend=趋势洞察/risk=风险预警/opportunity=机会发现）',
  `date` TIMESTAMP NOT NULL COMMENT '洞察时间',
  `text` TEXT DEFAULT NULL COMMENT '洞察内容',
  `action` VARCHAR(100) DEFAULT NULL COMMENT '行动指令（英文标识）',
  `action_text` VARCHAR(100) DEFAULT NULL COMMENT '行动描述（英文：continue=继续推进/optimize=优化/develop=开发）',
  `title` VARCHAR(255) DEFAULT NULL COMMENT '洞察标题（英文标识）',
  `description` TEXT DEFAULT NULL COMMENT '洞察详情',
  `recommendation` TEXT DEFAULT NULL COMMENT '建议措施',
  `priority` VARCHAR(10) DEFAULT NULL COMMENT '优先级（英文：high=高/medium=中/low=低）',
  `expected_outcome` TEXT DEFAULT NULL COMMENT '预期效果',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='洞察信息表';

-- 营销活动表
DROP TABLE IF EXISTS `marketing_activities`;
CREATE TABLE `marketing_activities` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` VARCHAR(255) DEFAULT NULL COMMENT '活动名称（英文：double11_promotion=双11促销等）',
  `participants` INT DEFAULT NULL COMMENT '参与人数（数值型，无单位）',
  `effect` VARCHAR(20) DEFAULT NULL COMMENT '活动效果（英文：excellent=优秀/good=良好/average=一般）',
  `engagement` FLOAT DEFAULT NULL COMMENT '参与度(%)',
  `conversion` FLOAT DEFAULT NULL COMMENT '转化率(%)',
  `date` TIMESTAMP NOT NULL COMMENT '活动时间',
  `priority` VARCHAR(20) DEFAULT NULL COMMENT '活动优先级（英文：high=高/medium=中/low=低）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='营销活动表';

-- 整体统计表
DROP TABLE IF EXISTS `stats`;
CREATE TABLE `stats` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `total_reviews` INT DEFAULT NULL COMMENT '总评论数',
  `positive_count` INT DEFAULT NULL COMMENT '正面评论数',
  `negative_count` INT DEFAULT NULL COMMENT '负面评论数',
  `positive_rate` FLOAT DEFAULT NULL COMMENT '正面率(%)',
  `trend_change` FLOAT DEFAULT NULL COMMENT '趋势变化(%)',
  `alert_count` INT DEFAULT NULL COMMENT '预警数',
  `hot_topic_count` INT DEFAULT NULL COMMENT '热话题数',
  `top_topic` VARCHAR(100) DEFAULT NULL COMMENT '热门话题（英文：new_product=新品发布）',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间（自动维护）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='整体统计表';

-- 热门话题表
DROP TABLE IF EXISTS `topics`;
CREATE TABLE `topics` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `rank` INT DEFAULT NULL COMMENT '话题排名',
  `name` VARCHAR(100) DEFAULT NULL COMMENT '话题名称（英文：new_product=新品发布/price_adjust=价格调整等）',
  `mentions` INT DEFAULT NULL COMMENT '提及数',
  `sentiment` VARCHAR(20) DEFAULT NULL COMMENT '情感倾向（英文：positive=正面/neutral=中性/negative=负面）',
  `trend` VARCHAR(20) DEFAULT NULL COMMENT '趋势（英文：rising=上升/stable=平稳/falling=下降）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='热门话题表';

-- 趋势洞察表
DROP TABLE IF EXISTS `trend_insights`;
CREATE TABLE `trend_insights` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `text` TEXT DEFAULT NULL COMMENT '趋势洞察内容',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='趋势洞察表';