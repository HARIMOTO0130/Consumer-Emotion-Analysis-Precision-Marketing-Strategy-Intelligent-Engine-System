<template>
  <div class="marketing-strategy-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>🎯 精准营销策略推荐</h1>
      <p class="subtitle">Precision Marketing Strategy Recommendation System</p>
    </div>

    <!-- 功能选项卡 -->
    <div class="tabs-container">
      <el-tabs v-model="activeTab" class="function-tabs">
        <el-tab-pane label="智能策略推荐" name="recommendation">
          <div class="tab-content">
            <!-- 策略推荐配置 -->
            <div class="recommendation-config">
              <h3>策略推荐配置</h3>
              <el-form :model="recommendationForm" label-width="120px" class="recommendation-form">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="目标受众">
                      <el-select
                        v-model="recommendationForm.audience"
                        placeholder="请选择目标受众"
                        style="width: 100%"
                      >
                        <el-option label="全体用户" value="all" />
                        <el-option label="新用户" value="new" />
                        <el-option label="老用户" value="existing" />
                        <el-option label="高价值用户" value="high_value" />
                        <el-option label="流失风险用户" value="churn_risk" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  
                  <el-col :span="12">
                    <el-form-item label="营销目标">
                      <el-select
                        v-model="recommendationForm.goal"
                        placeholder="请选择营销目标"
                        style="width: 100%"
                      >
                        <el-option label="提升转化率" value="conversion" />
                        <el-option label="增加客单价" value="average_order" />
                        <el-option label="提高复购率" value="repurchase" />
                        <el-option label="提升品牌知名度" value="brand_awareness" />
                        <el-option label="减少用户流失" value="retention" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="预算范围">
                      <el-select
                        v-model="recommendationForm.budget"
                        placeholder="请选择预算范围"
                        style="width: 100%"
                      >
                        <el-option label="低预算（<10万）" value="low" />
                        <el-option label="中预算（10-50万）" value="medium" />
                        <el-option label="高预算（>50万）" value="high" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  
                  <el-col :span="12">
                    <el-form-item label="活动周期">
                      <el-select
                        v-model="recommendationForm.period"
                        placeholder="请选择活动周期"
                        style="width: 100%"
                      >
                        <el-option label="短期（1-3天）" value="short" />
                        <el-option label="中期（4-7天）" value="medium" />
                        <el-option label="长期（8-30天）" value="long" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20">
                  <el-col :span="24">
                    <el-form-item label="关键因素">
                      <el-checkbox-group v-model="recommendationForm.factors">
                        <el-checkbox label="情感倾向" />
                        <el-checkbox label="购买历史" />
                        <el-checkbox label="浏览行为" />
                        <el-checkbox label="地域分布" />
                        <el-checkbox label="竞品活动" />
                        <el-checkbox label="季节因素" />
                      </el-checkbox-group>
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20" style="margin-top: 20px">
                  <el-col :span="8">
                    <el-button type="primary" @click="generateRecommendations" style="width: 100%">
                      生成策略推荐
                    </el-button>
                  </el-col>
                  <el-col :span="8">
                    <el-button @click="resetRecommendationForm" style="width: 100%">
                      重置
                    </el-button>
                  </el-col>
                </el-row>
              </el-form>
            </div>
            
            <!-- 策略推荐结果 -->
            <div class="recommendation-results">
              <h3>智能策略推荐结果</h3>
              <div class="strategy-cards">
                <div 
                  v-for="strategy in recommendedStrategies" 
                  :key="strategy.id" 
                  class="strategy-card"
                  :class="`priority-${strategy.priority}`"
                >
                  <div class="strategy-header">
                    <div class="strategy-title">
                      <span class="strategy-icon">{{ getStrategyIcon(strategy.type) }}</span>
                      <h4>{{ strategy.name }}</h4>
                    </div>
                    <div class="strategy-meta">
                      <span class="priority-tag" :class="`priority-${strategy.priority}`">
                        {{ strategy.priority === 'high' ? '高' : strategy.priority === 'medium' ? '中' : '低' }}优先级
                      </span>
                      <span class="expected-effect">{{ strategy.expectedEffect }}%</span>
                    </div>
                  </div>
                  <div class="strategy-content">
                    <p class="strategy-description">{{ strategy.description }}</p>
                    <div class="strategy-details">
                      <div class="detail-item">
                        <span class="detail-label">目标受众:</span>
                        <span class="detail-value">{{ strategy.audience }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="detail-label">预算估算:</span>
                        <span class="detail-value">{{ strategy.budget }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="detail-label">预期效果:</span>
                        <span class="detail-value">{{ strategy.expectedEffect }}%</span>
                      </div>
                    </div>
                  </div>
                  <div class="strategy-actions">
                    <el-button 
                      type="primary" 
                      @click="adoptStrategy(strategy.id)"
                    >
                      采纳策略
                    </el-button>
                    <el-button 
                      @click="previewStrategy(strategy.id)"
                    >
                      预览详情
                    </el-button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="营销活动管理" name="activities">
          <div class="tab-content">
            <!-- 活动创建表单 -->
            <div class="activity-create">
              <h3>创建营销活动</h3>
              <el-form :model="activityForm" label-width="120px" class="activity-form">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="活动名称">
                      <el-input
                        v-model="activityForm.name"
                        placeholder="请输入活动名称"
                        style="width: 100%"
                      />
                    </el-form-item>
                  </el-col>
                  
                  <el-col :span="12">
                    <el-form-item label="活动类型">
                      <el-select
                        v-model="activityForm.type"
                        placeholder="请选择活动类型"
                        style="width: 100%"
                      >
                        <el-option label="促销活动" value="promotion" />
                        <el-option label="新品发布" value="new_product" />
                        <el-option label="品牌合作" value="brand_cooperation" />
                        <el-option label="内容营销" value="content_marketing" />
                        <el-option label="社交媒体活动" value="social_media" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="开始时间">
                      <el-date-picker
                        v-model="activityForm.startTime"
                        type="datetime"
                        placeholder="选择开始时间"
                        style="width: 100%"
                      />
                    </el-form-item>
                  </el-col>
                  
                  <el-col :span="12">
                    <el-form-item label="结束时间">
                      <el-date-picker
                        v-model="activityForm.endTime"
                        type="datetime"
                        placeholder="选择结束时间"
                        style="width: 100%"
                      />
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="预算">
                      <el-input
                        v-model="activityForm.budget"
                        type="number"
                        placeholder="请输入预算"
                        style="width: 100%"
                      />
                    </el-form-item>
                  </el-col>
                  
                  <el-col :span="12">
                    <el-form-item label="目标受众">
                      <el-select
                        v-model="activityForm.audience"
                        placeholder="请选择目标受众"
                        style="width: 100%"
                      >
                        <el-option label="全体用户" value="all" />
                        <el-option label="新用户" value="new" />
                        <el-option label="老用户" value="existing" />
                        <el-option label="高价值用户" value="high_value" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20">
                  <el-col :span="24">
                    <el-form-item label="活动描述">
                      <el-input
                        v-model="activityForm.description"
                        type="textarea"
                        rows="3"
                        placeholder="请输入活动描述"
                        style="width: 100%"
                      />
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20" style="margin-top: 20px">
                  <el-col :span="8">
                    <el-button type="primary" @click="createActivity" style="width: 100%">
                      创建活动
                    </el-button>
                  </el-col>
                  <el-col :span="8">
                    <el-button @click="resetActivityForm" style="width: 100%">
                      重置
                    </el-button>
                  </el-col>
                </el-row>
              </el-form>
            </div>
            
            <!-- 活动列表 -->
            <div class="activity-list-section">
              <h3>营销活动列表</h3>
              <el-table :data="marketingActivities" style="width: 100%">
                <el-table-column prop="name" label="活动名称" width="200" />
                <el-table-column prop="type" label="活动类型" width="150">
                  <template #default="{ row }">
                    <el-tag :type="getTypeColor(row.type)">
                      {{ getTypeName(row.type) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="startTime" label="开始时间" width="180" />
                <el-table-column prop="endTime" label="结束时间" width="180" />
                <el-table-column prop="status" label="状态" width="100">
                  <template #default="{ row }">
                    <el-tag :type="getStatusColor(row.status)">
                      {{ row.status }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="budget" label="预算" width="120" />
                <el-table-column prop="participants" label="参与人数" width="100" />
                <el-table-column label="操作" width="200">
                  <template #default="{ row }">
                    <el-button 
                      size="small" 
                      type="primary" 
                      @click="viewActivityDetail(row.id)"
                    >
                      查看详情
                    </el-button>
                    <el-button 
                      size="small" 
                      type="danger" 
                      @click="cancelActivity(row.id)"
                      :disabled="row.status === '已结束' || row.status === '已取消'"
                    >
                      取消活动
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="效果分析" name="analysis">
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
                  <!-- 这里可以集成ECharts图表 -->
                  <div class="chart-placeholder">
                    <p>营销效果趋势图表</p>
                    <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAwIiBoZWlnaHQ9IjQwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48L3N2Zz4=" alt="效果趋势图" style="width: 100%; height: 300px; background: #f5f5f5; border: 1px solid #ddd; border-radius: 4px;" />
                  </div>
                </div>
              </div>
              
              <!-- 受众分析 -->
              <div class="audience-analysis">
                <h4>受众分析</h4>
                <el-table :data="audienceAnalysis" style="width: 100%">
                  <el-table-column prop="segment" label="用户群体" width="150" />
                  <el-table-column prop="count" label="参与人数" width="120" />
                  <el-table-column prop="engagement" label="参与度" width="120">
                    <template #default="{ row }">
                      <div class="progress-bar">
                        <div class="progress-fill" :style="{ width: row.engagement + '%' }"></div>
                        <span class="progress-text">{{ row.engagement }}%</span>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column prop="conversion" label="转化率" width="120">
                    <template #default="{ row }">
                      <div class="progress-bar">
                        <div class="progress-fill" :style="{ width: row.conversion + '%' }"></div>
                        <span class="progress-text">{{ row.conversion }}%</span>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column prop="revenue" label="贡献收入" width="150" />
                </el-table>
              </div>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="智能洞察" name="insights">
          <div class="tab-content">
            <!-- 智能洞察列表 -->
            <div class="insights-section">
              <h3>智能营销洞察</h3>
              <div class="insights-list">
                <div 
                  v-for="insight in marketingInsights" 
                  :key="insight.id" 
                  class="insight-card"
                  :class="`type-${insight.type}`"
                >
                  <div class="insight-header">
                    <div class="insight-type">
                      <span class="type-icon">{{ getInsightIcon(insight.type) }}</span>
                      <span class="type-label">{{ getInsightTypeLabel(insight.type) }}</span>
                    </div>
                    <div class="insight-meta">
                      <span class="insight-date">{{ insight.date }}</span>
                      <span class="insight-priority" :class="`priority-${insight.priority}`">
                        {{ insight.priority }}
                      </span>
                    </div>
                  </div>
                  <div class="insight-content">
                    <h4 class="insight-title">{{ insight.title }}</h4>
                    <p class="insight-description">{{ insight.description }}</p>
                    <div class="insight-data">
                      <div class="data-item">
                        <span class="data-label">影响范围:</span>
                        <span class="data-value">{{ insight.impact }}</span>
                      </div>
                      <div class="data-item">
                        <span class="data-label">置信度:</span>
                        <span class="data-value">{{ insight.confidence }}%</span>
                      </div>
                    </div>
                  </div>
                  <div class="insight-recommendation">
                    <h5>推荐行动:</h5>
                    <p>{{ insight.recommendation }}</p>
                    <el-button 
                      type="primary" 
                      size="small" 
                      @click="takeInsightAction(insight.id)"
                    >
                      执行行动
                    </el-button>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 趋势预测 -->
            <div class="trend-prediction">
              <h3>趋势预测</h3>
              <div class="prediction-cards">
                <div class="prediction-card">
                  <div class="prediction-title">
                    <span class="prediction-icon">📈</span>
                    <h4>情感趋势预测</h4>
                  </div>
                  <div class="prediction-content">
                    <p>基于历史数据和当前趋势，预测未来7天的情感变化趋势。</p>
                    <div class="prediction-trend">
                      <div class="trend-item">
                        <span class="trend-date">今天</span>
                        <span class="trend-value positive">72.5%</span>
                      </div>
                      <div class="trend-item">
                        <span class="trend-date">1天后</span>
                        <span class="trend-value positive">73.2%</span>
                      </div>
                      <div class="trend-item">
                        <span class="trend-date">3天后</span>
                        <span class="trend-value positive">74.8%</span>
                      </div>
                      <div class="trend-item">
                        <span class="trend-date">7天后</span>
                        <span class="trend-value positive">76.5%</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="prediction-card">
                  <div class="prediction-title">
                    <span class="prediction-icon">🎯</span>
                    <h4>营销效果预测</h4>
                  </div>
                  <div class="prediction-content">
                    <p>基于历史活动数据，预测不同类型营销活动的预期效果。</p>
                    <div class="prediction-types">
                      <div class="type-item">
                        <span class="type-name">促销活动</span>
                        <span class="type-effect positive">+25%</span>
                      </div>
                      <div class="type-item">
                        <span class="type-name">新品发布</span>
                        <span class="type-effect positive">+35%</span>
                      </div>
                      <div class="type-item">
                        <span class="type-name">品牌合作</span>
                        <span class="type-effect positive">+20%</span>
                      </div>
                      <div class="type-item">
                        <span class="type-name">内容营销</span>
                        <span class="type-effect positive">+15%</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 响应式数据
const activeTab = ref('recommendation')

// 推荐表单
const recommendationForm = ref({
  audience: '',
  goal: '',
  budget: '',
  period: '',
  factors: []
})

// 活动表单
const activityForm = ref({
  name: '',
  type: '',
  startTime: '',
  endTime: '',
  budget: '',
  audience: '',
  description: ''
})

// 分析表单
const analysisForm = ref({
  activityId: '',
  timeRange: 'activity',
  dimension: 'overall'
})

// 推荐策略
const recommendedStrategies = ref([
  {
    id: 1,
    name: '新用户注册礼包',
    type: 'acquisition',
    description: '针对新用户推出注册礼包，提高注册转化率和首次购买率',
    audience: '新用户',
    budget: '5-10万',
    expectedEffect: 35,
    priority: 'high'
  },
  {
    id: 2,
    name: '老用户复购优惠',
    type: 'retention',
    description: '针对30天未复购的老用户推出专属优惠，提高复购率',
    audience: '老用户',
    budget: '10-15万',
    expectedEffect: 28,
    priority: 'medium'
  },
  {
    id: 3,
    name: '高价值用户专属活动',
    type: 'loyalty',
    description: '为高价值用户打造专属活动，提升品牌忠诚度和客单价',
    audience: '高价值用户',
    budget: '15-20万',
    expectedEffect: 42,
    priority: 'high'
  },
  {
    id: 4,
    name: '流失风险用户挽回',
    type: 'retention',
    description: '针对流失风险用户推出个性化挽回方案，减少用户流失',
    audience: '流失风险用户',
    budget: '8-12万',
    expectedEffect: 22,
    priority: 'medium'
  }
])

// 营销活动
const marketingActivities = ref([
  {
    id: 1,
    name: '双11促销活动',
    type: 'promotion',
    startTime: '2023-11-11 00:00:00',
    endTime: '2023-11-11 23:59:59',
    status: '已结束',
    budget: '50万',
    participants: '2.4万'
  },
  {
    id: 2,
    name: '新品上市推广',
    type: 'new_product',
    startTime: '2023-10-15 00:00:00',
    endTime: '2023-10-22 23:59:59',
    status: '已结束',
    budget: '30万',
    participants: '1.8万'
  },
  {
    id: 3,
    name: '品牌联合营销',
    type: 'brand_cooperation',
    startTime: '2023-09-20 00:00:00',
    endTime: '2023-09-27 23:59:59',
    status: '已结束',
    budget: '20万',
    participants: '1.2万'
  },
  {
    id: 4,
    name: '圣诞节活动',
    type: 'promotion',
    startTime: '2023-12-20 00:00:00',
    endTime: '2023-12-25 23:59:59',
    status: '进行中',
    budget: '25万',
    participants: '8.5千'
  }
])

// 效果指标
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

// 受众分析
const audienceAnalysis = ref([
  { segment: '新用户', count: 1200, engagement: 75, conversion: 8, revenue: '23.4万' },
  { segment: '老用户', count: 2800, engagement: 92, conversion: 15, revenue: '78.6万' },
  { segment: '高价值用户', count: 500, engagement: 98, conversion: 25, revenue: '45.2万' },
  { segment: '流失风险用户', count: 800, engagement: 65, conversion: 6, revenue: '12.8万' }
])

// 营销洞察
const marketingInsights = ref([
  {
    id: 1,
    type: 'opportunity',
    title: '年轻用户对互动功能兴趣浓厚',
    description: '数据显示18-30岁用户对产品的互动功能表现出浓厚兴趣，参与度比其他年龄段高35%',
    date: '2023-12-01',
    priority: '高',
    impact: '高',
    confidence: 92,
    recommendation: '开发更多社交互动功能，针对年轻用户推出互动营销活动'
  },
  {
    id: 2,
    type: 'risk',
    title: '价格敏感度在周末明显增加',
    description: '数据分析显示周末时段用户价格敏感度明显增加，转化率下降15%',
    date: '2023-11-28',
    priority: '中',
    impact: '中',
    confidence: 85,
    recommendation: '在周末推出限时特价活动，提高周末转化率'
  },
  {
    id: 3,
    type: 'trend',
    title: '移动端用户占比持续上升',
    description: '移动端用户占比从65%上升到82%，且移动端用户的平均购买频次高于PC端',
    date: '2023-11-25',
    priority: '高',
    impact: '高',
    confidence: 95,
    recommendation: '优化移动端用户体验，加大移动端营销投入'
  },
  {
    id: 4,
    type: 'opportunity',
    title: '产品质量相关正面情感增加',
    description: '最近一个月，关于产品质量的正面评价增加了15%，主要集中在产品性能和耐用性方面',
    date: '2023-11-20',
    priority: '中',
    impact: '中',
    confidence: 88,
    recommendation: '加大产品质量相关的营销宣传，突出产品性能优势'
  }
])

// 方法
const getStrategyIcon = (type) => {
  const icons = {
    acquisition: '🎯',
    retention: '🔒',
    loyalty: '💎',
    reactivation: '⚡'
  }
  return icons[type] || '🎯'
}

const adoptStrategy = (strategyId) => {
  ElMessage.success('策略已采纳！')
}

const previewStrategy = (strategyId) => {
  ElMessage.info('预览策略详情')
}

const generateRecommendations = () => {
  if (!recommendationForm.value.audience || !recommendationForm.value.goal) {
    ElMessage.warning('请选择目标受众和营销目标')
    return
  }
  
  ElMessage.success('策略推荐生成成功！')
}

const resetRecommendationForm = () => {
  recommendationForm.value = {
    audience: '',
    goal: '',
    budget: '',
    period: '',
    factors: []
  }
}

const createActivity = () => {
  if (!activityForm.value.name || !activityForm.value.type) {
    ElMessage.warning('请填写活动名称和类型')
    return
  }
  
  const newActivity = {
    id: marketingActivities.value.length + 1,
    name: activityForm.value.name,
    type: activityForm.value.type,
    startTime: activityForm.value.startTime || new Date().toISOString(),
    endTime: activityForm.value.endTime || new Date().toISOString(),
    status: '未开始',
    budget: activityForm.value.budget || '0',
    participants: '0'
  }
  
  marketingActivities.value.push(newActivity)
  ElMessage.success('活动创建成功！')
  resetActivityForm()
}

const resetActivityForm = () => {
  activityForm.value = {
    name: '',
    type: '',
    startTime: '',
    endTime: '',
    budget: '',
    audience: '',
    description: ''
  }
}

const viewActivityDetail = (activityId) => {
  ElMessage.info('查看活动详情')
}

const cancelActivity = (activityId) => {
  const activity = marketingActivities.value.find(a => a.id === activityId)
  if (activity) {
    activity.status = '已取消'
    ElMessage.success('活动已取消！')
  }
}

const getTypeColor = (type) => {
  const colors = {
    promotion: 'success',
    new_product: 'primary',
    brand_cooperation: 'warning',
    content_marketing: 'info',
    social_media: 'danger'
  }
  return colors[type] || 'info'
}

const getTypeName = (type) => {
  const names = {
    promotion: '促销活动',
    new_product: '新品发布',
    brand_cooperation: '品牌合作',
    content_marketing: '内容营销',
    social_media: '社交媒体活动'
  }
  return names[type] || '其他活动'
}

const getStatusColor = (status) => {
  const colors = {
    '未开始': 'info',
    '进行中': 'warning',
    '已结束': 'success',
    '已取消': 'danger'
  }
  return colors[status] || 'info'
}

const analyzeEffect = () => {
  if (!analysisForm.value.activityId) {
    ElMessage.warning('请选择活动')
    return
  }
  
  ElMessage.success('效果分析完成！')
}

const getInsightIcon = (type) => {
  const icons = {
    opportunity: '💡',
    risk: '⚠️',
    trend: '📈',
    insight: '🧠'
  }
  return icons[type] || '🧠'
}

const getInsightTypeLabel = (type) => {
  const labels = {
    opportunity: '机会发现',
    risk: '风险预警',
    trend: '趋势洞察',
    insight: '智能洞察'
  }
  return labels[type] || '智能洞察'
}

const takeInsightAction = (insightId) => {
  ElMessage.success('已执行洞察建议！')
}

// 退出登录方法
const handleLogout = () => {
  console.log('退出登录')
  router.push('/login')
}

// 生命周期
onMounted(() => {
  console.log('精准营销策略推荐组件已挂载')
})
</script>

<style scoped>
.marketing-strategy-container {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

/* 导航栏样式 */
.dashboard-header {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
  padding: 20px;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.header-left {
  flex: 1;
}

.system-title {
  font-size: 24px;
  margin-bottom: 5px;
  color: #333;
  font-weight: bold;
}

.system-subtitle {
  font-size: 14px;
  color: #666;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  font-size: 24px;
}

.user-details {
  text-align: right;
}

.username {
  display: block;
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

.user-role {
  display: block;
  font-size: 12px;
  color: #666;
}

.btn-logout {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 16px;
  background-color: #f5f5f5;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.btn-logout:hover {
  background-color: #e8e8e8;
  border-color: #1890ff;
}

.logout-icon {
  font-size: 16px;
}

.header-nav {
  border-top: 1px solid #e8e8e8;
  padding-top: 20px;
}

.main-nav {
  display: flex;
  gap: 20px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  text-decoration: none;
  color: #666;
  border-radius: 4px;
  transition: all 0.3s;
  border: 1px solid transparent;
}

.nav-item:hover {
  color: #1890ff;
  background-color: #f0f9ff;
  border-color: #e6f7ff;
}

.nav-item.active {
  color: #1890ff;
  background-color: #e6f7ff;
  border-color: #91d5ff;
  font-weight: bold;
}

.nav-icon {
  font-size: 16px;
}

.nav-label {
  font-size: 14px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 30px 0;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.page-header h1 {
  font-size: 28px;
  margin-bottom: 10px;
  color: #333;
}

.subtitle {
  font-size: 16px;
  color: #666;
}

.tabs-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.function-tabs {
  margin-top: 20px;
}

.tab-content {
  padding: 20px 0;
}

.recommendation-config,
.activity-create,
.analysis-config,
.recommendation-results,
.activity-list-section,
.analysis-results,
.insights-section,
.trend-prediction {
  margin-bottom: 30px;
}

.recommendation-config h3,
.activity-create h3,
.analysis-config h3,
.recommendation-results h3,
.activity-list-section h3,
.analysis-results h3,
.insights-section h3,
.trend-prediction h3 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 2px solid #1890ff;
  padding-bottom: 10px;
}

.recommendation-form,
.activity-form,
.analysis-form {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.strategy-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

.strategy-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.strategy-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.strategy-card.priority-high {
  border-left: 4px solid #ff4d4f;
}

.strategy-card.priority-medium {
  border-left: 4px solid #faad14;
}

.strategy-card.priority-low {
  border-left: 4px solid #52c41a;
}

.strategy-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.strategy-title {
  display: flex;
  align-items: center;
}

.strategy-icon {
  font-size: 24px;
  margin-right: 10px;
}

.strategy-title h4 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.strategy-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.priority-tag {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 5px;
}

.priority-tag.priority-high {
  background-color: #fff2f0;
  color: #ff4d4f;
}

.priority-tag.priority-medium {
  background-color: #fffbe6;
  color: #faad14;
}

.priority-tag.priority-low {
  background-color: #f6ffed;
  color: #52c41a;
}

.expected-effect {
  font-size: 14px;
  font-weight: bold;
  color: #1890ff;
}

.strategy-description {
  margin-bottom: 15px;
  color: #666;
  line-height: 1.5;
}

.strategy-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 10px;
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 2px;
}

.detail-value {
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

.strategy-actions {
  display: flex;
  gap: 10px;
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
  background-color: #1890ff;
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

.insights-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

.insight-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.insight-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.insight-card.type-opportunity {
  border-left: 4px solid #52c41a;
}

.insight-card.type-risk {
  border-left: 4px solid #ff4d4f;
}

.insight-card.type-trend {
  border-left: 4px solid #1890ff;
}

.insight-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.insight-type {
  display: flex;
  align-items: center;
}

.type-icon {
  font-size: 16px;
  margin-right: 8px;
}

.type-label {
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

.insight-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.insight-date {
  font-size: 12px;
  color: #999;
}

.insight-priority {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.insight-priority.priority-高 {
  background-color: #fff2f0;
  color: #ff4d4f;
}

.insight-priority.priority-中 {
  background-color: #fffbe6;
  color: #faad14;
}

.insight-priority.priority-低 {
  background-color: #f6ffed;
  color: #52c41a;
}

.insight-title {
  font-size: 16px;
  margin-bottom: 10px;
  color: #333;
}

.insight-description {
  margin-bottom: 15px;
  color: #666;
  line-height: 1.5;
}

.insight-data {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.data-item {
  display: flex;
  flex-direction: column;
}

.data-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 2px;
}

.data-value {
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

.insight-recommendation {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #e8e8e8;
}

.insight-recommendation h5 {
  font-size: 14px;
  margin-bottom: 10px;
  color: #333;
}

.insight-recommendation p {
  margin-bottom: 15px;
  color: #666;
  line-height: 1.5;
}

.prediction-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.prediction-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.prediction-title {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.prediction-icon {
  font-size: 24px;
  margin-right: 10px;
}

.prediction-title h4 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.prediction-content p {
  margin-bottom: 15px;
  color: #666;
  line-height: 1.5;
}

.prediction-trend,
.prediction-types {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.trend-item,
.type-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: white;
  border-radius: 4px;
}

.trend-date,
.type-name {
  color: #333;
}

.trend-value,
.type-effect {
  font-weight: bold;
}

.trend-value.positive,
.type-effect.positive {
  color: #52c41a;
}

.trend-value.negative,
.type-effect.negative {
  color: #ff4d4f;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .strategy-cards,
  .insights-list,
  .prediction-cards,
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