-- 转换中间文件，存档用
/*
 Navicat Premium Dump SQL

 Source Server         : test-sqlite
 Source Server Type    : SQLite
 Source Server Version : 3045000 (3.45.0)
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3045000 (3.45.0)
 File Encoding         : 65001

 Date: 28/01/2026 17:13:03
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for alerts
-- ----------------------------
DROP TABLE IF EXISTS "alerts";
CREATE TABLE "alerts" (
  "id" INTEGER NOT NULL,
  "title" VARCHAR,
  "type" VARCHAR,
  "severity" VARCHAR,
  "date" VARCHAR,
  "status" VARCHAR,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS "comments";
CREATE TABLE "comments" (
  "id" INTEGER NOT NULL,
  "text" VARCHAR,
  "source" VARCHAR,
  "time" VARCHAR,
  "emotion" VARCHAR,
  "sentiment" VARCHAR,
  "intensity" VARCHAR,
  "timestamp" VARCHAR,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for emotion_distribution
-- ----------------------------
DROP TABLE IF EXISTS "emotion_distribution";
CREATE TABLE "emotion_distribution" (
  "id" INTEGER NOT NULL,
  "channel" VARCHAR,
  "positive" INTEGER,
  "negative" INTEGER,
  "positive_percent" FLOAT,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for insights
-- ----------------------------
DROP TABLE IF EXISTS "insights";
CREATE TABLE "insights" (
  "id" INTEGER NOT NULL,
  "type" VARCHAR,
  "date" VARCHAR,
  "text" VARCHAR,
  "action" VARCHAR,
  "action_text" VARCHAR,
  "title" VARCHAR,
  "description" VARCHAR,
  "recommendation" VARCHAR,
  "priority" VARCHAR,
  "expected_outcome" VARCHAR,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for marketing_activities
-- ----------------------------
DROP TABLE IF EXISTS "marketing_activities";
CREATE TABLE "marketing_activities" (
  "id" INTEGER NOT NULL,
  "name" VARCHAR,
  "participants" VARCHAR,
  "effect" VARCHAR,
  "engagement" FLOAT,
  "conversion" FLOAT,
  "date" VARCHAR,
  "priority" VARCHAR,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for stats
-- ----------------------------
DROP TABLE IF EXISTS "stats";
CREATE TABLE "stats" (
  "id" INTEGER NOT NULL,
  "total_reviews" INTEGER,
  "positive_count" INTEGER,
  "negative_count" INTEGER,
  "positive_rate" FLOAT,
  "trend_change" FLOAT,
  "alert_count" INTEGER,
  "hot_topic_count" INTEGER,
  "top_topic" VARCHAR,
  "updated_at" DATETIME,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for topics
-- ----------------------------
DROP TABLE IF EXISTS "topics";
CREATE TABLE "topics" (
  "id" INTEGER NOT NULL,
  "rank" INTEGER,
  "name" VARCHAR,
  "mentions" INTEGER,
  "sentiment" VARCHAR,
  "trend" VARCHAR,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for trend_insights
-- ----------------------------
DROP TABLE IF EXISTS "trend_insights";
CREATE TABLE "trend_insights" (
  "id" INTEGER NOT NULL,
  "text" VARCHAR,
  PRIMARY KEY ("id")
);

PRAGMA foreign_keys = true;
