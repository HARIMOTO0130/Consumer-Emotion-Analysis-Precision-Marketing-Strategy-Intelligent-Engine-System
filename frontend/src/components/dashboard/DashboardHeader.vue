<template>
  <div class="dashboard-title-section">
    <div class="title-content">
      <div style="display: flex;gap: 8px">
        <mdicon name="dashboard" size="35" />
        <div>
          <h2>情感分析仪表盘总览</h2>
          <p class="dashboard-subtitle">实时监控消费者情感变化与营销策略效果</p>
        </div>
      </div>
      
    </div>
    <div class="dashboard-controls">
      <div class="time-control">
        <span class="control-label" id="time-range-label">
          <mdicon name="calendar-month" size="20" />
          时间范围
        </span>
        <el-select 
          v-model="timeRange"
          class="time-select"
          placeholder="选择时间范围"
          @change="handleTimeChange"
          :disabled="loading"
          aria-labelledby="time-range-label"
          aria-describedby="time-range-description"
          tabindex="0"
        >
          <el-option label="最近1小时" value="1h" :aria-label="'时间范围：最近1小时'" />
          <el-option label="最近24小时" value="24h" :aria-label="'时间范围：最近24小时'" />
          <el-option label="最近7天" value="7d" :aria-label="'时间范围：最近7天'" />
          <el-option label="最近30天" value="30d" :aria-label="'时间范围：最近30天'" />
        </el-select>
        <span id="time-range-description" class="sr-only">选择数据统计的时间范围</span>
      </div>
      <button 
        class="btn-refresh" 
        @click="refreshData" 
        :disabled="loading"
        :aria-label="loading ? '数据加载中' : '刷新数据'"
        :aria-busy="loading"
        tabindex="0"
        role="button"
      >
        <mdicon name="refresh" size="20" color="#fff" />
        <span>{{ loading ? '加载中...' : '刷新数据' }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { ElSelect, ElOption } from 'element-plus'
import mdicon from 'vue-material-design-icons'

const props = defineProps({
  timeRange: {
    type: String,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['time-change', 'refresh'])

const handleTimeChange = (value) => {
  emit('time-change', value)
}

const refreshData = () => {
  emit('refresh')
}
</script>

<style scoped>
.dashboard-title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 24px;
}

.title-content h2 {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 12px 0;
  color: #2c3e50;
  line-height: 1.2;
}

.dashboard-subtitle {
  font-size: 16px;
  color: #7f8c8d;
  margin: 0;
  line-height: 1.4;
}

.dashboard-controls {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}

.time-control {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  background-color: rgba(24, 144, 255, 0.05);
  border-radius: 8px;
}

.control-label {
  align-items: center;
  display: flex;
  gap:4px;
  font-size: 14px;
  font-weight: 500;
  color: #546e7a;
  white-space: nowrap;
}

.time-select {
  min-width: 160px;
}

.btn-refresh {
  background-color: var(--color-primary);
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.btn-refresh:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
}

.btn-refresh:disabled {
  background: #d9d9d9;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* 响应式适配 */
@media (max-width: 1200px) {
  .dashboard-title-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .dashboard-controls {
    justify-content: space-around;
  }
}

@media (max-width: 992px) {
  .dashboard-controls {
    justify-content: space-around;
    align-items: stretch;
    gap: 10px;
  }
  
  .time-control {
    justify-content: space-between;
  }
}

@media (max-width: 768px) {
  .dashboard-title-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .title-content h2 {
    font-size: 24px;
  }
  
  .dashboard-subtitle {
    font-size: 14px;
  }
  
  .dashboard-controls {
    justify-content: space-around;
    align-items: stretch;
    gap: 10px;
  }
  
  .time-control {
    justify-content: space-between;
  }
}

@media (max-width: 576px) {
  .title-content h2 {
    font-size: 20px;
  }
  
  .dashboard-subtitle {
    font-size: 12px;
  }
  
  .dashboard-controls {
    justify-content: space-around;
    align-items: stretch;
    gap: 10px;
  }
  
  .time-control {
    justify-content: space-between;
  }
}

/* 无障碍访问样式 */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
  .btn-refresh {
    border: 2px solid #000;
  }
}
</style>