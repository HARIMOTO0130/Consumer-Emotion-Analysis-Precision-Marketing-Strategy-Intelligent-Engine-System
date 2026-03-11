<template>
  <el-card class="data-card" shadow="hover" @click="openMarketingEffectDialog">
    <template #header>
      <div class="card-header">
        <div class="header-title">
          <mdicon name="rocket-launch-outline" size="28"/>
          <h3>营销效果速览</h3>
          <span class="marketing-count">{{ marketingActivities.length }}</span>
        </div>
      </div>
    </template>
    <div class="marketing-list">
      <div 
        v-for="activity in marketingActivities" 
        :key="activity.id" 
        :class="['marketing-item', `priority-${activity.priority}`]"
      >
        <div class="marketing-content">
          <div class="marketing-header">
            <span class="activity-name">{{ activity.name }}</span>
            <span class="effect-badge" :class="`badge-${activity.effect}`">
              效果: {{ getEffectName(activity.effect) }}
            </span>
          </div>
          <div class="marketing-details">
            <div class="detail-item">
              <span class="detail-label">参与度:</span>
              <span class="detail-value">{{ activity.engagement }}%</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">转化率:</span>
              <span class="detail-value">{{ activity.conversion }}%</span>
            </div>
          </div>
          <div class="marketing-time">{{ formatDate(activity.date,"yyyy-mm-dd") }}</div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { ElCard } from 'element-plus'
import mdicon from 'vue-material-design-icons'

const props = defineProps({
  marketingActivities: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['open-marketing-effect'])

const openMarketingEffectDialog = () => {
  emit('open-marketing-effect')
}

const getEffectName = (effect) => {
  const names = {
    'excellent': '优秀',
    'good': '良好',
    'average': '一般',
    'poor': '较差'
  }
  return names[effect] || effect
}

const formatDate = (date, format) => {
  // 简单的日期格式化函数
  const d = new Date(date)
  if (format === 'yyyy-mm-dd') {
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
  }
  return date
}
</script>

<style scoped>
.data-card {
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.data-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.card-header {
  padding: 16px 20px;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.header-title .card-icon {
  font-size: 20px;
  margin: 0;
}

.header-title h3 {
  font-size: 18px;
  font-weight: bold;
  margin: 0;
  color: #333;
}

.header-title .marketing-count {
  background: var(--color-error);
  color: white;
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 10px;
  margin-left: 10px;
  font-weight: bold;
}

.marketing-list {
  padding: 0 20px 20px;
}

.marketing-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.marketing-item:hover {
  background: #f0f0f0;
  transform: translateX(5px);
}

.marketing-item.priority-high {
  border-left: 4px solid var(--color-danger);
}

.marketing-item.priority-medium {
  border-left: 4px solid var(--color-warning);
}

.marketing-item.priority-low {
  border-left: 4px solid var(--color-info);
}

.marketing-icon {
  font-size: 20px;
  min-width: 30px;
}

.marketing-content {
  flex: 1;
}

.marketing-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 10px;
}

.activity-name {
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

.effect-badge {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}

.badge-excellent {
  background: var(--color-success-hover);
  color: white;
}

.badge-good {
  background: var(--color-primary-hover);
  color: #fff;
}

.badge-average {
  background: var(--color-warning-hover);
  color: #fff;
}

.badge-poor {
  background: var(--color-danger-hover);
  color: #fff;
}

.marketing-details {
  display: flex;
  gap: 20px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.detail-label {
  font-size: 12px;
  color: #666;
}

.detail-value {
  font-size: 12px;
  font-weight: 500;
  color: #333;
}

.marketing-time {
  font-size: 12px;
  color: #999;
  justify-self: end;
}
</style>