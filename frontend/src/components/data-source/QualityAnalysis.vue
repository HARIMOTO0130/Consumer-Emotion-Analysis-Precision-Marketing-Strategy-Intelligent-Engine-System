<template>
  <div class="tab-content">
    <div class="quality-section">
      <h3>数据质量分析</h3>
      <div class="quality-metrics">
        <div class="metric-card">
          <div class="metric-title">完整性</div>
          <div class="metric-value">{{ qualityMetrics.completeness }}%</div>
          <div class="metric-bar">
            <div 
              class="bar-fill" 
              :style="{ width: qualityMetrics.completeness + '%', background: getQualityColor(qualityMetrics.completeness) }"
            ></div>
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-title">准确性</div>
          <div class="metric-value">{{ qualityMetrics.accuracy }}%</div>
          <div class="metric-bar">
            <div 
              class="bar-fill" 
              :style="{ width: qualityMetrics.accuracy + '%', background: getQualityColor(qualityMetrics.accuracy) }"
            ></div>
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-title">时效性</div>
          <div class="metric-value">{{ qualityMetrics.timeliness }}%</div>
          <div class="metric-bar">
            <div 
              class="bar-fill" 
              :style="{ width: qualityMetrics.timeliness + '%', background: getQualityColor(qualityMetrics.timeliness) }"
            ></div>
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-title">一致性</div>
          <div class="metric-value">{{ qualityMetrics.consistency }}%</div>
          <div class="metric-bar">
            <div 
              class="bar-fill" 
              :style="{ width: qualityMetrics.consistency + '%', background: getQualityColor(qualityMetrics.consistency) }"
            ></div>
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-title">有效性</div>
          <div class="metric-value">{{ qualityMetrics.validity }}%</div>
          <div class="metric-bar">
            <div 
              class="bar-fill" 
              :style="{ width: qualityMetrics.validity + '%', background: getQualityColor(qualityMetrics.validity) }"
            ></div>
          </div>
        </div>
      </div>
      
      <!-- 数据质量问题 -->
      <div class="quality-issues">
        <h3>数据质量问题</h3>
        <el-table :data="qualityIssues" style="width: 100%">
          <el-table-column prop="type" label="问题类型"   />
          <el-table-column prop="description" label="问题描述" />
          <el-table-column prop="severity" label="严重程度"  >
            <template #default="{ row }">
              <el-tag :type="row.severity === '高' ? 'danger' : row.severity === '中' ? 'warning' : 'info'">
                {{ row.severity }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="count" label="数量"   />
          <el-table-column prop="status" label="状态"  >
            <template #default="{ row }">
              <el-tag :type="row.status === '已处理' ? 'success' : row.status === '处理中' ? 'warning' : 'danger'">
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { ElTable, ElTableColumn, ElTag } from 'element-plus'

const props = defineProps({
  qualityMetrics: {
    type: Object,
    required: true
  },
  qualityIssues: {
    type: Array,
    required: true
  }
})

const emit = defineEmits([])

const getQualityColor = (value) => {
  if (value >= 90) return '#52c41a'
  if (value >= 70) return '#73d13d'
  if (value >= 50) return '#ffd666'
  return '#ff7875'
}
</script>

<style scoped>
.quality-section h3,
.quality-issues h3 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 2px solid var(--color-primary-hover);
  padding-bottom: 10px;
}

.quality-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.metric-card {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.metric-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.metric-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.metric-bar {
  height: 8px;
  background-color: #e8e8e8;
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.quality-issues {
  margin-top: 30px;
}
</style>