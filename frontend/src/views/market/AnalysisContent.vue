<template>
  <div class="tab-content">
    <div class="analysis-config">
      <h3>效果分析配置</h3>
      <el-form :model="analysisForm" label-width="120px" class="analysis-form">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="活动选择">
              <el-select v-model="analysisForm.activityId" placeholder="请选择活动" style="width: 100%" :disabled="analyzing">
                <el-option v-for="activity in marketingActivities" :key="activity.id" :label="activity.name" :value="activity.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="时间范围">
              <el-select v-model="analysisForm.timeRange" placeholder="请选择时间范围" style="width: 100%" :disabled="analyzing">
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
              <el-select v-model="analysisForm.dimension" placeholder="请选择分析维度" style="width: 100%" :disabled="analyzing">
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
            <el-button 
              type="primary" 
              @click="analyzeEffect" 
              :loading="analyzing" 
              :disabled="analyzing"
              style="width: 100%"
            >
              {{ analyzing ? '深度分析中...' : '开始分析' }}
            </el-button>
          </el-col>
        </el-row>
      </el-form>
    </div>

    <div class="analysis-results" v-loading="analyzing" element-loading-text="正在计算大数据指标...">
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

      <div class="effect-trend">
        <h4>效果趋势分析</h4>
        <div class="chart-container" ref="chartContainerRef">
          <div id="trend-chart" style="width: 100%; height: 200px;"></div>
        </div>
      </div>

      <div class="audience-analysis">
        <h4>受众分析</h4>
        <el-table :data="audienceAnalysis" style="width: 100%">
          <el-table-column prop="segment" label="用户群体" />
          <el-table-column prop="count" label="参与人数" />
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
          <el-table-column prop="revenue" label="贡献收入" />
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { initTrendChart } from '@components/strategy-recommend/tendency-chart'

// 状态控制：是否正在分析
const analyzing = ref(false)

const analysisForm = ref({
  activityId: '',
  timeRange: 'activity',
  dimension: 'overall'
})

const marketingActivities = ref([
  { id: 1, name: '双11促销活动' },
  { id: 2, name: '新品上市推广' },
  { id: 3, name: '品牌联合营销' }
])

const effectMetrics = ref({
  engagement: 85,
  engagementChange: 5.2,
  conversion: 12,
  conversionChange: 2.1,
  averageOrder: 299,
  averageOrderChange: 8.5,
  roi: 320,
  roiChange: 15.3
})

const audienceAnalysis = ref([
  { segment: '新用户', count: 23, engagement: 75, conversion: 8, revenue: '219' },
  { segment: '老用户', count: 87, engagement: 92, conversion: 47, revenue: '768' },
  { segment: '高价值用户', count: 76, engagement: 98, conversion: 25, revenue: '23' },
  { segment: '流失风险用户', count: 8, engagement: 65, conversion: 6, revenue: '213' }
])

const chartContainerRef = ref(null)
let chartInstance = null
let resizeObserver = null

const generateFakeData = (form) => {
  const { activityId, timeRange } = form
  let baseEngagement = 80
  let baseConversion = 15
  let baseAvgOrder = 280
  let baseRoi = 300

  switch (activityId) {
    case 1: 
      baseEngagement += 10; baseConversion -= 3; baseAvgOrder += 20; baseRoi += 50
      break
    case 2: 
      baseEngagement += 2; baseConversion += 8; baseAvgOrder += 10; baseRoi += 30
      break
    case 3: 
      baseEngagement -= 5; baseConversion += 2; baseAvgOrder += 50; baseRoi += 20
      break
  }

  let volatility = timeRange === '7d' ? 1.5 : (timeRange === '30d' ? 1.2 : 0.8)
  const randomFactor = (min, max) => min + Math.random() * (max - min)

  const engagement = Math.round(baseEngagement + randomFactor(-5 * volatility, 5 * volatility))
  const conversion = Math.round((baseConversion + randomFactor(-3 * volatility, 3 * volatility)) * 10) / 10
  const avgOrder = Math.round(baseAvgOrder + randomFactor(-20 * volatility, 20 * volatility))
  const roi = Math.round(baseRoi + randomFactor(-30 * volatility, 30 * volatility))

  const newMetrics = {
    engagement: Math.min(99, Math.max(40, engagement)),
    engagementChange: Math.round((randomFactor(-8, 12) * volatility) * 10) / 10,
    conversion: Math.min(40, Math.max(3, conversion)),
    conversionChange: Math.round((randomFactor(-5, 10) * volatility) * 10) / 10,
    averageOrder: Math.min(600, Math.max(150, avgOrder)),
    averageOrderChange: Math.round((randomFactor(-6, 8) * volatility) * 10) / 10,
    roi: Math.min(500, Math.max(100, roi)),
    roiChange: Math.round((randomFactor(-10, 20) * volatility) * 10) / 10
  }

  const segmentRatios = { '新用户': 0.2, '老用户': 0.4, '高价值用户': 0.3, '流失风险用户': 0.1 }
  const segmentFactors = {
    '新用户': { engagement: 0.9, conversion: 0.7, avgOrder: 0.8 },
    '老用户': { engagement: 1.1, conversion: 1.2, avgOrder: 1.1 },
    '高价值用户': { engagement: 1.2, conversion: 1.3, avgOrder: 1.5 },
    '流失风险用户': { engagement: 0.8, conversion: 0.5, avgOrder: 0.9 }
  }

  const newAudience = Object.entries(segmentRatios).map(([segment, ratio]) => {
    const factor = segmentFactors[segment]
    const count = Math.round((200 + randomFactor(-50, 150) * volatility) * ratio)
    const segEng = Math.min(99, Math.max(30, Math.round(newMetrics.engagement * factor.engagement + randomFactor(-5, 5))))
    const segConv = Math.min(50, Math.max(2, Math.round((newMetrics.conversion * factor.conversion + randomFactor(-3, 3)) * 10) / 10))
    const revenue = Math.round(count * (segConv / 100) * (newMetrics.averageOrder * factor.avgOrder))
    return { segment, count, engagement: segEng, conversion: segConv, revenue: revenue.toString() }
  })

  const days = timeRange === '7d' ? 7 : (timeRange === '30d' ? 30 : 14)
  const trendDates = Array.from({ length: days }, (_, i) => {
    const d = new Date(); d.setDate(d.getDate() - (days - 1 - i))
    return `${(d.getMonth() + 1).toString().padStart(2, '0')}-${d.getDate().toString().padStart(2, '0')}`
  })
  const trendValues = Array.from({ length: days }, () => Math.min(99, Math.max(30, Math.round((newMetrics.engagement + (Math.random() - 0.5) * 12) * 10) / 10)))

  return { effectMetrics: newMetrics, audienceAnalysis: newAudience, trendDates, trendValues }
}

const analyzeEffect = () => {
  if (!analysisForm.value.activityId) {
    ElMessage.warning('请选择活动')
    return
  }

  // 1. 进入加载状态
  analyzing.value = true

  // 2. 模拟 5 秒异步计算
  setTimeout(() => {
    try {
      const data = generateFakeData(analysisForm.value)
      
      // 更新响应式数据
      effectMetrics.value = data.effectMetrics
      audienceAnalysis.value = data.audienceAnalysis

      // 更新图表
      if (chartInstance) {
        chartInstance.setOption({
          xAxis: { data: data.trendDates },
          series: [{ data: data.trendValues }]
        })
      }
      ElMessage.success('深度分析完成！')
    } catch (err) {
      ElMessage.error('分析计算失败')
    } finally {
      // 3. 5秒后关闭加载状态
      analyzing.value = false
    }
  }, 5000) 
}

onMounted(async () => {
  await nextTick()
  chartInstance = initTrendChart()
  if (chartContainerRef.value && chartInstance?.resize) {
    resizeObserver = new ResizeObserver(() => chartInstance.resize())
    resizeObserver.observe(chartContainerRef.value)
  }
})

onUnmounted(() => {
  resizeObserver?.disconnect()
  chartInstance?.dispose?.()
})
</script>

<style scoped>
.tab-content { padding: 20px 0; }
.analysis-config, .analysis-results { margin-bottom: 30px; }
.analysis-config h3, .analysis-results h3 {
  font-size: 18px; margin-bottom: 20px; color: #333;
  border-bottom: 2px solid #409eff; padding-bottom: 10px;
}
.analysis-form { background-color: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 30px; }
.effect-metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
.metric-card { background-color: #f9f9f9; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #ebeef5; }
.metric-title { font-size: 14px; color: #666; margin-bottom: 10px; }
.metric-value { font-size: 24px; font-weight: bold; color: #333; margin-bottom: 5px; }
.metric-change { font-size: 12px; }
.metric-change.positive { color: #52c41a; }
.metric-change.negative { color: #ff4d4f; }
.effect-trend, .audience-analysis { margin-top: 30px; }
.effect-trend h4, .audience-analysis h4 { font-size: 16px; margin-bottom: 15px; color: #333; }
.chart-container { background-color: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 30px; }
.progress-bar { position: relative; height: 20px; background-color: #e8e8e8; border-radius: 10px; overflow: hidden; margin-bottom: 5px; }
.progress-fill { height: 100%; background-color: #409eff; border-radius: 10px; transition: width 0.3s ease; }
.progress-text { position: absolute; top: 0; left: 50%; transform: translateX(-50%); line-height: 20px; font-size: 12px; font-weight: bold; color: white; text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3); }
@media (max-width: 768px) { .effect-metrics { grid-template-columns: 1fr; } }
</style>