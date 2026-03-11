<template>
  <el-card class="insight-card" shadow="hover" @click="openInsightSummaryDialog">
    <template #header>
      <div class="card-header">
        <div class="header-title">
          <mdicon name="mindfulness-outline-rounded" size="28"/>
          <h3>智能洞察摘要</h3>
        </div>
      </div>
    </template>
    <div class="insight-content">
      <div class="insight-item" v-for="insight in insights" :key="insight.id">
        <div class="insight-header">
          <span class="insight-type">{{ getActionTypeName(insight.type) }}</span>
          <span class="insight-date">{{ formatDate(insight.date,"yyyy-mm-dd") }}</span>
        </div>
        <div class="insight-text">{{ insight.text }}</div>
        <div class="insight-action">
          <el-button 
            size="small" 
            type="primary" 
            @click.stop="takeAction(insight.action)"
            :aria-label="`执行${insight.actionText}操作`"
            tabindex="0"
          >
            {{ insight.actionText }}
          </el-button>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { ElCard, ElButton } from 'element-plus'
import mdicon from 'vue-material-design-icons'

const props = defineProps({
  insights: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['open-insight-summary', 'take-action'])

const openInsightSummaryDialog = () => {
  emit('open-insight-summary')
}

const takeAction = (action) => {
  emit('take-action', action)
}

const getActionTypeName = (type) => {
  const names = {
    'trend_insight': '趋势洞察',
    'risk_warning': '风险预警',
    'opportunity_discovery': '机会发现'
  }
  return names[type] || type
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
.insight-card {
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.insight-card:hover {
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

.insight-content {
  padding: 0 20px 20px;
}

.insight-item {
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.insight-item:hover {
  background: #f0f0f0;
  transform: translateX(5px);
}

.insight-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 10px;
}

.insight-type {
  background: var(--color-primary-dark);
  color: white;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}

.insight-date {
  font-size: 12px;
  color: #999;
}

.insight-text {
  font-size: 14px;
  color: #333;
  margin-bottom: 12px;
  line-height: 1.4;
}

.insight-action {
  display: flex;
  justify-content: flex-end;
}
</style>