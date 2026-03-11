<template>
  <div class="tab-content">
    <!-- 效果分析配置 -->
    <div class="analysis-config">
      <h3>效果分析配置</h3>
      <el-form :model="analysisForm" label-width="120px" class="analysis-form">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="活动选择">
              <el-select
                v-model="analysisForm.activityId"
                placeholder="请选择活动"
                style="width: 100%"
              >
                <el-option 
                  v-for="activity in marketingActivities" 
                  :key="activity.id" 
                  :label="activity.name" 
                  :value="activity.id" 
                />
              </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="时间范围">
              <el-select
                v-model="analysisForm.timeRange"
                placeholder="请选择时间范围"
                style="width: 100%"
              >
                <el-option label="活动期间" value="activity" />
                <el-option label="最近7天" value="7d" />
                <el-option label="最近30天" value="30d" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="分析维度">
              <el-select
                v-model="analysisForm.dimension"
                placeholder="请选择分析维度"
                style="width: 100%"
              >
                <el-option label="整体效果" value="overall" />
                <el-option label="受众分析" value="audience" />
                <el-option label="渠道分析" value="channel" />
                <el-option label="时间趋势" value="time" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" style="margin-top: 20px">
          <el-col :span="8">
            <el-button type="primary" @click="analyzeEffect" style="width: 100%">
              开始分析
            </el-button>
          </el-col>
        </el-row>
      </el-form>
    </div>
    
    <!-- 效果分析结果 -->
    <div class="analysis-results">
      <h3>效果分析结果</h3>
      <div class="effect-metrics">
        <div class="metric-card">
          <div class="metric-title">参与度</div>
          <div class="metric-value">{{ effectMetrics.engagement }}%</div>
          <div class="metric-change" :class="effectMetrics.engagementChange >= 0 ? 'positive' : 'negative'">
            {{ effectMetrics.engagementChange >= 0 ? '+' : '' }}{{ effectMetrics.engagementChange }}%
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-title">转化率</div>
          <div class="metric-value">{{ effectMetrics.conversion }}%</div>
          <div class="metric-change" :class="effectMetrics.conversionChange >= 0 ? 'positive' : 'negative'">
            {{ effectMetrics.conversionChange >= 0 ? '+' : '' }}{{ effectMetrics.conversionChange }}%
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-title">客单价</div>
          <div class="metric-value">{{ effectMetrics.averageOrder }}</div>
          <div class="metric-change" :class="effectMetrics.averageOrderChange >= 0 ? 'positive' : 'negative'">
            {{ effectMetrics.averageOrderChange >= 0 ? '+' : '' }}{{ effectMetrics.averageOrderChange }}%
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-title">ROI</div>
          <div class="metric-value">{{ effectMetrics.roi }}%</div>
          <div class="metric-change" :class="effectMetrics.roiChange >= 0 ? 'positive' : 'negative'">
            {{ effectMetrics.roiChange >= 0 ? '+' : '' }}{{ effectMetrics.roiChange }}%
          </div>
        </div>
      </div>
      
      <!-- 效果趋势图表 -->
      <div class="effect-trend">
        <h4>效果趋势分析</h4>
        <div class="chart-container">
          <div class="chart-placeholder">
              <div class="chart-container" style="width: 100%; height: 200px;">
                <div id="trend-chart" style="width: 100%; height: 100%;"></div>
              </div>
          </div>
        </div>
      </div>
      
      <!-- 受众分析 -->
      <div class="audience-analysis">
        <h4>受众分析</h4>
        <el-table :data="audienceAnalysis" style="width: 100%">
          <el-table-column prop="segment" label="用户群体"/>
          <el-table-column prop="count" label="参与人数"/>
          <el-table-column prop="engagement" label="参与度">
            <template #default="{ row }">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: row.engagement + '%' }"></div>
                <span class="progress-text">{{ row.engagement }}%</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="conversion" label="转化率">
            <template #default="{ row }">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: row.conversion + '%' }"></div>
                <span class="progress-text">{{ row.conversion }}%</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="revenue" label="贡献收入"/>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { ElForm, ElFormItem, ElSelect, ElOption, ElButton, ElTable, ElTableColumn, ElRow, ElCol } from 'element-plus'

const props = defineProps({
  analysisForm: {
    type: Object,
    required: true
  },
  effectMetrics: {
    type: Object,
    required: true
  },
  audienceAnalysis: {
    type: Array,
    required: true
  },
  marketingActivities: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['analyze-effect'])

const analyzeEffect = () => {
  emit('analyze-effect')
}
</script>

<style scoped>
.analysis-config h3,
.analysis-results h3 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 2px solid var(--color-primary-hover);
  padding-bottom: 10px;
}

.analysis-form {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.effect-metrics {
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
  margin-bottom: 5px;
}

.metric-change {
  font-size: 12px;
}

.metric-change.positive {
  color: #52c41a;
}

.metric-change.negative {
  color: #ff4d4f;
}

.effect-trend,
.audience-analysis {
  margin-top: 30px;
}

.effect-trend h4,
.audience-analysis h4 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #333;
}

.chart-container {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.progress-bar {
  position: relative;
  height: 20px;
  background-color: #e8e8e8;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 5px;
}

.progress-fill {
  height: 100%;
  background-color: var(--color-primary-hover);
  border-radius: 10px;
  transition: width 0.3s ease;
}

.progress-text {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  line-height: 20px;
  font-size: 12px;
  font-weight: bold;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .effect-metrics {
    grid-template-columns: 1fr;
  }
  
  .el-row {
    flex-direction: column;
  }
  
  .el-col {
    width: 100% !important;
    margin-bottom: 15px;
  }
}
</style>