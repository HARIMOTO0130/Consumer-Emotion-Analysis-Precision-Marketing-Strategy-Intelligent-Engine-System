<template>
  <el-card class="data-card" shadow="hover" @click="openTrendAnalysisDialog">
    <template #header>
      <div class="card-header">
        <div class="header-title">
          <mdicon name="grouped-bar-chart" size="28"/>
          <h3>情感趋势分析</h3>
        </div>
        <div class="chart-tabs">
          <button 
            v-for="tab in chartTabs" 
            :key="tab.id"
            :class="['chart-tab', { active: activeChart === tab.id }]"
            @click.stop="activeChart = tab.id"
            :aria-label="`切换到${tab.label}图表`"
            :aria-selected="activeChart === tab.id"
            role="tab"
            tabindex="0"
            @keydown.enter="activeChart = tab.id"
            @keydown.space.prevent="activeChart = tab.id"
          >
            {{ tab.label }}
          </button>
        </div>
      </div>
    </template>
    <div class="chart-container">
      <!-- 情感趋势图表 -->
      <div v-if="activeChart === 'emotion'" class="chart-content">
        <div class="chart-header">
          <h4>近24小时情感趋势变化</h4>
        </div>
        <v-chart class="chart" :option="emotionTrendOption" autoresize />
      </div>
      
      <!-- 营销效果图表 -->
      <div v-if="activeChart === 'marketing'" class="chart-content">
        <div class="chart-header">
          <h4>近期营销活动效果分析</h4>
        </div>
        <v-chart class="chart" :option="marketingEffectOption" autoresize />
      </div>
      
      <!-- 情感分类图表 -->
      <div v-if="activeChart === 'classification'" class="chart-content">
        <div class="chart-header">
          <h4>情感分类分布</h4>
        </div>
        <v-chart class="chart" :option="emotionClassificationOption" autoresize />
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue'
import { ElCard } from 'element-plus'
import VChart from 'vue-echarts'
import mdicon from 'vue-material-design-icons'

const props = defineProps({
  chartTabs: {
    type: Array,
    required: true
  },
  emotionTrendOption: {
    type: Object,
    required: true
  },
  marketingEffectOption: {
    type: Object,
    required: true
  },
  emotionClassificationOption: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['open-trend-analysis'])

const activeChart = ref('emotion')

const openTrendAnalysisDialog = () => {
  emit('open-trend-analysis')
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

.chart-tabs {
  display: flex;
  gap: 10px;
}

.chart-tab {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f0f0f0;
  color: #666;
  border: none;
  outline: none;
}

.chart-tab:hover {
  background: #e0e0e0;
}

.chart-tab.active {
  background: var(--color-primary-dark);
  color: white;
}

.chart-content {
  margin-top: 20px;
}

.chart-content h4 {
  font-size: 16px;
  font-weight: bold;
  margin: 0 0 16px 0;
  color: #333;
}

.chart {
  height: 300px;
}
</style>