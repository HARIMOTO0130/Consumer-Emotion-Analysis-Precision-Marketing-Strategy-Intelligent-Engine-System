<template>
  <div class="overview-grid">
    <div class="overview-card card-total" @click="openEmotionOverviewDialog">
      <div class="card-icon"><mdicon name="chat-outline-rounded" size="50" color="var(--color-primary)"/></div>
      <div class="card-content">
        <div class="card-value">{{ stats.totalReviews }}</div>
        <div class="card-label">今日新增评论</div>
        <div class="card-status">
          <span class="status-tag positive">正面 {{ stats.positiveCount }}</span>
          <span class="status-tag negative">负面 {{ stats.negativeCount }}</span>
        </div>
      </div>
    </div>
    
    <div class="overview-card card-success" @click="openTrendAnalysisDialog">
      <div class="card-icon"><mdicon name="show-chart" size="50" color="var(--color-success)"/></div>
      <div class="card-content">
        <div class="card-value">{{ stats.positiveRate }}%</div>
        <div class="card-label">整体正面率</div>
        <div class="card-trend positive status-tag">
          <span class="trend-icon"> 较昨日 +{{ stats.trendChange }}%</span>
        </div>
      </div>
    </div>
    
    <div class="overview-card card-warning" @click="openAlertMonitoringDialog">
      <div class="card-icon"><mdicon name="warning-outline-rounded" size="50" color="var(--color-warning)"/></div>
      <div class="card-content">
        <div class="card-value">{{ stats.alertCount }}</div>
        <div class="card-label">舆情预警数量</div>
        <div class="card-trend status-tag negative">
          <span class="trend-icon">需立即关注</span>
        </div>
      </div>
    </div>
    
    <div class="overview-card card-environment" @click="openTopicHotnessDialog">
      <div class="card-icon"><mdicon name="local-fire-department-outline-rounded" size="50" color="var(--color-danger)"/></div>
      <div class="card-content">
        <div class="card-value">{{ stats.hotTopicCount }}</div>
        <div class="card-label">热点话题数量</div>
        <div class="topic-info">
          <span class="topic-item">最热: {{ stats.topTopic }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { ElTag } from 'element-plus'
import mdicon from 'vue-material-design-icons'

const props = defineProps({
  stats: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['open-emotion-overview', 'open-trend-analysis', 'open-alert-monitoring', 'open-topic-hotness'])

const openEmotionOverviewDialog = () => {
  emit('open-emotion-overview')
}

const openTrendAnalysisDialog = () => {
  emit('open-trend-analysis')
}

const openAlertMonitoringDialog = () => {
  emit('open-alert-monitoring')
}

const openTopicHotnessDialog = () => {
  emit('open-topic-hotness')
}
</script>

<style scoped>
.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.overview-card {
  background: white;
  border-radius: 16px;
  padding: 28px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.overview-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--color-primary-hover), #36cfc9);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.overview-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  border-color: rgba(24, 144, 255, 0.2);
}

.overview-card:hover::before {
  transform: scaleX(1);
}

.card-total:hover {
  border-color: rgba(82, 196, 26, 0.3);
}

.card-success:hover {
  border-color: rgba(115, 209, 61, 0.3);
}

.card-warning:hover {
  border-color: rgba(250, 173, 20, 0.3);
}

.card-environment:hover {
  border-color: rgba(250, 140, 22, 0.3);
}

.card-total::before {
  background: linear-gradient(90deg, #52c41a, #73d13d);
}

.card-success::before {
  background: linear-gradient(90deg, #73d13d, #95de64);
}

.card-warning::before {
  background: linear-gradient(90deg, #faad14, #ffd666);
}

.card-environment::before {
  background: linear-gradient(90deg, #fa8c16, #ffad46);
}

.card-total:hover {
  border-color: #52c41a;
}

.card-success:hover {
  border-color: #73d13d;
}

.card-warning:hover {
  border-color: #faad14;
}

.card-environment:hover {
  border-color: #fa8c16;
}

.card-icon {
  font-size: 42px;
  margin-bottom: 20px;
  display: block;
}

.card-content {
  position: relative;
  z-index: 1;
}

.card-content .card-value {
  font-size: 36px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 12px;
  line-height: 1.1;
}

.card-content .card-label {
  font-size: 18px;
  color: #7f8c8d;
  margin-bottom: 16px;
  font-weight: 400;
}

.card-status {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}

.status-tag {
  padding: 6px 16px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.status-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.status-tag.positive {
  background: rgba(82, 196, 26, 0.15);
  color: #52c41a;
}

.status-tag.negative {
  background: rgba(255, 77, 79, 0.15);
  color: #ff4d4f;
}

.card-trend {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  padding: 8px 12px;
  background-color: rgba(0, 0, 0, 0.02);
  border-radius: 8px;
  width: fit-content;
  transition: all 0.3s ease;
}

.card-trend:hover {
  background-color: rgba(0, 0, 0, 0.04);
  transform: translateY(-2px);
}

.card-trend.positive {
  color: #52c41a;
}

.card-trend.warning {
  color: #faad14;
}

.card-trend.neutral {
  color: #1890ff;
}

.topic-info {
  font-size: 15px;
  color: #7f8c8d;
  line-height: 1.4;
}

.topic-item {
  font-weight: 600;
  color: #2c3e50;
  display: inline-block;
  margin-left: 4px;
  padding: 4px 8px;
  background-color: rgba(24, 144, 255, 0.1);
  border-radius: 6px;
  transition: all 0.3s ease;
}

.topic-item:hover {
  background-color: rgba(24, 144, 255, 0.2);
  transform: translateY(-2px);
}

/* 响应式适配 */
@media (max-width: 992px) {
  .overview-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
  }
  
  .overview-card {
    padding: 20px;
  }
  
  .card-icon {
    font-size: 30px;
    margin-bottom: 12px;
  }
  
  .card-content .card-value {
    font-size: 28px;
  }
}

@media (max-width: 768px) {
  .overview-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .overview-card {
    padding: 16px;
  }
  
  .card-icon {
    font-size: 28px;
  }
  
  .card-content .card-value {
    font-size: 22px;
  }
  
  .card-content .card-label {
    font-size: 13px;
  }
  
  .card-status {
    gap: 8px;
  }
  
  .status-tag {
    padding: 3px 10px;
    font-size: 11px;
  }
}

@media (max-width: 576px) {
  .overview-card {
    padding: 14px;
  }
  
  .card-icon {
    font-size: 24px;
    margin-bottom: 10px;
  }
  
  .card-content .card-value {
    font-size: 20px;
  }
  
  .card-content .card-label {
    font-size: 12px;
    margin-bottom: 8px;
  }
  
  .card-trend {
    font-size: 12px;
  }
  
  .topic-info {
    font-size: 12px;
  }
}
</style>