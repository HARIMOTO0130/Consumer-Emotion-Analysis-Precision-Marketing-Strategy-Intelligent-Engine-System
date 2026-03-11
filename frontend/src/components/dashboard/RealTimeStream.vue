<template>
  <el-card class="data-card" shadow="hover" @click="openRealTimeStreamDialog">
    <template #header>
      <div class="card-header">
        <div class="header-title">
          <mdicon name="area-chart" size="28" />
          <h3>实时情感监测流</h3>
        </div>
        <div class="stream-controls">
          <el-button 
            size="small" 
            @click.stop="toggleStream"
            :aria-label="streamPaused ? '播放实时情感监测流' : '暂停实时情感监测流'"
            tabindex="0"
          >
            {{ streamPaused ? '播放' : '暂停' }}
          </el-button>
        </div>
      </div>
    </template>
    <div class="stream-container">
      <div class="stream-item" v-for="item in recentComments" :key="item.id">
        <div class="stream-emotion" :class="item.emotion">
          <span v-if="item.emotion === 'positive'">😊</span>
          <span v-if="item.emotion === 'neutral'">😐</span>
          <span v-if="item.emotion === 'negative'">😞</span>
        </div>
        <div class="stream-content">
          <div class="stream-text">{{ item.text }}</div>
          <div class="stream-meta">
            <span class="stream-source">{{ getChannelName(item.source) }}</span>
            <span class="stream-time">{{ formatDate(item.time,"yyyy-mm") }}</span>
          </div>
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
  recentComments: {
    type: Array,
    required: true
  },
  streamPaused: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['open-real-time-stream', 'toggle-stream'])

const openRealTimeStreamDialog = () => {
  emit('open-real-time-stream')
}

const toggleStream = () => {
  emit('toggle-stream')
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

const formatDate = (time, format) => {
  // 简单的日期格式化函数
  const date = new Date(time)
  if (format === 'yyyy-mm') {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
  }
  return time
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

.stream-controls {
  display: flex;
  gap: 10px;
}

.stream-container {
  max-height: 300px;
  overflow-y: auto;
  padding-right: 8px;
}

.stream-container::-webkit-scrollbar {
  width: 6px;
}

.stream-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 3px;
}

.stream-container::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.stream-container::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

.stream-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.stream-item:hover {
  background: #f0f0f0;
  transform: translateX(5px);
}

.stream-item:nth-child(odd) {
  background-color: rgba(24, 144, 255, 0.02);
}

.stream-item:nth-child(odd):hover {
  background-color: rgba(24, 144, 255, 0.05);
}

.stream-emotion {
  font-size: 20px;
  min-width: 30px;
}

.stream-content {
  flex: 1;
}

.stream-text {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
  line-height: 1.4;
}

.stream-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #999;
}

.stream-source {
  font-weight: 500;
  background-color: rgba(0, 0, 0, 0.05);
  padding: 2px 8px;
  border-radius: 12px;
}

.stream-time {
  font-family: monospace;
}
</style>