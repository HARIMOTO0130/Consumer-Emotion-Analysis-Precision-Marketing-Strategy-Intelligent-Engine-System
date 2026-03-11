<template>
  <el-card class="data-card" shadow="hover" @click="openEmotionDistributionDialog">
    <template #header>
      <div class="card-header">
        <div class="header-title">
          <mdicon name="insert-chart-outline" size="28"/>
          <h3>情感分布分析</h3>
        </div>
        <div class="header-subtitle">按渠道、人群、产品线的情感分布对比</div>
      </div>
    </template>
    <div class="emotion-distribution">
      <div 
        v-for="(item, index) in emotionDistribution" 
        :key="item.channel" 
        class="dist-item"
      >
        <div class="dist-info">
          <div class="dist-range">
            <span>{{ getChannelName(item.channel) }}</span>
          </div>
          <div class="dist-count">{{ item.positive }}/{{ item.negative }}</div>
          <div class="dist-percentage">正面: {{ item.positivePercent }}%</div>
        </div>
        <div class="dist-bar-container">
          <div class="dist-bar">
            <div 
              class="bar-fill" 
              :style="{ width: item.positivePercent + '%', background: getEmotionColor(index) }"
            ></div>
          </div>
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
  emotionDistribution: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['open-emotion-distribution'])

const openEmotionDistributionDialog = () => {
  emit('open-emotion-distribution')
}

const getChannelName = (channel) => {
  const names = {
    '微博': '微博',
    '微信': '微信',
    '抖音': '抖音',
    '电商': '电商'
  }
  return names[channel] || channel
}

const getEmotionColor = (index) => {
  const colors = ['var(--color-primary)', 'var(--color-success)', 'var(--color-error)', 'var(--color-warning)']
  return colors[index] || '#52c41a'
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

.header-subtitle {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.emotion-distribution {
  padding: 0 20px 20px;
}

.dist-item {
  margin-bottom: 20px;
}

.dist-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 10px;
}

.dist-range {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.range-icon {
  font-size: 16px;
}

.dist-count {
  font-size: 14px;
  color: #666;
}

.dist-percentage {
  font-size: 14px;
  font-weight: 500;
  color: #52c41a;
}

.dist-bar-container {
  width: 100%;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.dist-bar {
  width: 100%;
  height: 100%;
}

.bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease;
}
</style>