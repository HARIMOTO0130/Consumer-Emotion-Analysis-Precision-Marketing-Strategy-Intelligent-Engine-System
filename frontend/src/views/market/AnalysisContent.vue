<template>
  <div class="tab-content">
    <!-- 效果分析配置 -->
    <div class="analysis-config">
      <h3>效果分析配置</h3>
      <el-form :model="analysisForm" label-width="120px" class="analysis-form">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="活动选择">
              <el-select v-model="analysisForm.activityId" placeholder="请选择活动" style="width: 100%">
                <el-option v-for="activity in marketingActivities" :key="activity.id" :label="activity.name" :value="activity.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="时间范围">
              <el-select v-model="analysisForm.timeRange" placeholder="请选择时间范围" style="width: 100%">
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
              <el-select v-model="analysisForm.dimension" placeholder="请选择分析维度" style="width: 100%">
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
            <el-button type="primary" @click="analyzeEffect" style="width: 100%">开始分析</el-button>
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
        <div class="chart-container" ref="chartContainerRef">
          <div id="trend-chart" style="width: 100%; height: 200px;"></div>
        </div>
      </div>

      <!-- 受众分析 -->
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

// 图表容器 ref
const chartContainerRef = ref(null)
// 存储图表实例
let chartInstance = null
// 存储 ResizeObserver 实例
let resizeObserver = null

/**
 * 根据表单选择生成逼真的随机数据（包含指标、受众和趋势）
 */
const generateFakeData = (form) => {
  const { activityId, timeRange, dimension } = form

  // 基础值（根据不同活动调整）
  let baseEngagement = 80
  let baseConversion = 15
  let baseAvgOrder = 280
  let baseRoi = 300

  // 活动影响
  switch (activityId) {
    case 1: // 双11促销 -> 参与度高，转化稍低
      baseEngagement += 10
      baseConversion -= 3
      baseAvgOrder += 20
      baseRoi += 50
      break
    case 2: // 新品上市 -> 转化率高，参与度中等
      baseEngagement += 2
      baseConversion += 8
      baseAvgOrder += 10
      baseRoi += 30
      break
    case 3: // 品牌联合 -> 客单价高，参与度稍低
      baseEngagement -= 5
      baseConversion += 2
      baseAvgOrder += 50
      baseRoi += 20
      break
    default: // 未选择活动时使用默认
      break
  }

  // 时间范围影响（波动系数）
  let volatility = 1.0
  if (timeRange === '7d') {
    volatility = 1.5 // 短期波动大
  } else if (timeRange === '30d') {
    volatility = 1.2 // 中期波动中等
  } else {
    volatility = 0.8 // 活动期间较稳定
  }

  // 生成指标值
  const randomFactor = (min, max) => min + Math.random() * (max - min)

  const engagement = Math.round(baseEngagement + randomFactor(-5 * volatility, 5 * volatility))
  const conversion = Math.round((baseConversion + randomFactor(-3 * volatility, 3 * volatility)) * 10) / 10
  const avgOrder = Math.round(baseAvgOrder + randomFactor(-20 * volatility, 20 * volatility))
  const roi = Math.round(baseRoi + randomFactor(-30 * volatility, 30 * volatility))

  // 变化率（环比），正负随机，但总趋势与指标值有一定关联
  const engagementChange = Math.round((randomFactor(-8, 12) * volatility) * 10) / 10
  const conversionChange = Math.round((randomFactor(-5, 10) * volatility) * 10) / 10
  const avgOrderChange = Math.round((randomFactor(-6, 8) * volatility) * 10) / 10
  const roiChange = Math.round((randomFactor(-10, 20) * volatility) * 10) / 10

  const newMetrics = {
    engagement: Math.min(99, Math.max(40, engagement)),
    engagementChange,
    conversion: Math.min(40, Math.max(3, conversion)),
    conversionChange,
    averageOrder: Math.min(600, Math.max(150, avgOrder)),
    averageOrderChange: avgOrderChange,
    roi: Math.min(500, Math.max(100, roi)),
    roiChange
  }

  // 生成受众分析数据（基于指标）
  const totalParticipants = Math.round(200 + randomFactor(-50, 150) * volatility)

  const segmentRatios = {
    '新用户': 0.2,
    '老用户': 0.4,
    '高价值用户': 0.3,
    '流失风险用户': 0.1
  }

  const segmentFactors = {
    '新用户': { engagement: 0.9, conversion: 0.7, avgOrder: 0.8 },
    '老用户': { engagement: 1.1, conversion: 1.2, avgOrder: 1.1 },
    '高价值用户': { engagement: 1.2, conversion: 1.3, avgOrder: 1.5 },
    '流失风险用户': { engagement: 0.8, conversion: 0.5, avgOrder: 0.9 }
  }

  const newAudience = []
  for (const [segment, ratio] of Object.entries(segmentRatios)) {
    const factor = segmentFactors[segment]
    const count = Math.round(totalParticipants * ratio * (0.9 + 0.2 * Math.random()))

    let segEngagement = newMetrics.engagement * factor.engagement + randomFactor(-5, 5)
    segEngagement = Math.min(99, Math.max(30, Math.round(segEngagement)))

    let segConversion = newMetrics.conversion * factor.conversion + randomFactor(-3, 3)
    segConversion = Math.min(50, Math.max(2, Math.round(segConversion * 10) / 10))

    let segAvgOrder = newMetrics.averageOrder * factor.avgOrder + randomFactor(-20, 20)
    segAvgOrder = Math.max(50, Math.round(segAvgOrder))

    const revenue = Math.round(count * (segConversion / 100) * segAvgOrder)

    newAudience.push({
      segment,
      count,
      engagement: segEngagement,
      conversion: segConversion,
      revenue: revenue.toString()
    })
  }

  // 生成趋势数据（参与度随时间变化）
  const days = timeRange === '7d' ? 7 : timeRange === '30d' ? 30 : 14
  const trendDates = []
  const trendValues = []
  const today = new Date()
  for (let i = days - 1; i >= 0; i--) {
    const d = new Date(today)
    d.setDate(d.getDate() - i)
    const month = (d.getMonth() + 1).toString().padStart(2, '0')
    const day = d.getDate().toString().padStart(2, '0')
    trendDates.push(`${month}-${day}`)
  }

  const baseTrendValue = newMetrics.engagement
  for (let i = 0; i < days; i++) {
    // 在基础值上加上随机波动，并确保在合理范围内
    let val = baseTrendValue + (Math.random() - 0.5) * 12 // 波动范围 ±6
    val = Math.min(99, Math.max(30, Math.round(val * 10) / 10))
    trendValues.push(val)
  }

  return {
    effectMetrics: newMetrics,
    audienceAnalysis: newAudience,
    trendDates,
    trendValues
  }
}

const analyzeEffect = () => {
  if (!analysisForm.value.activityId) {
    ElMessage.warning('请选择活动')
    return
  }

  // 生成假数据
  const { effectMetrics: newMetrics, audienceAnalysis: newAudience, trendDates, trendValues } = generateFakeData(analysisForm.value)

  // 更新响应式数据
  effectMetrics.value = newMetrics
  audienceAnalysis.value = newAudience

  // 更新图表数据
  if (chartInstance) {
    chartInstance.setOption({
      xAxis: { data: trendDates },
      series: [{ data: trendValues }]
    })
  }

  ElMessage.success('效果分析完成！')
}

onMounted(async () => {
  // 等待 DOM 完全渲染后再初始化图表，确保容器尺寸已计算
  await nextTick()

  // 初始化图表并保存实例
  chartInstance = initTrendChart() // 假设返回 echarts 实例

  // 如果 initTrendChart 不返回实例，则手动获取
  // const chartDom = document.getElementById('trend-chart')
  // chartInstance = echarts.init(chartDom)

  // 使用 ResizeObserver 监听容器尺寸变化
  if (chartContainerRef.value && chartInstance && typeof chartInstance.resize === 'function') {
    resizeObserver = new ResizeObserver(() => {
      chartInstance.resize()
    })
    resizeObserver.observe(chartContainerRef.value)
  }
})

onUnmounted(() => {
  // 清理 ResizeObserver
  if (resizeObserver) {
    resizeObserver.disconnect()
    resizeObserver = null
  }
  // 销毁图表实例（可选）
  if (chartInstance && typeof chartInstance.dispose === 'function') {
    chartInstance.dispose()
  }
})
</script>

<style scoped>
.tab-content {
  padding: 20px 0;
}
.analysis-config,
.analysis-results {
  margin-bottom: 30px;
}
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
@media (max-width: 768px) {
  .effect-metrics {
    grid-template-columns: 1fr;
  }
}
</style>