<template>
  <div class="data-source-container">

    <!-- 功能选项卡 -->
    <div class="tabs-container">
          <div class="">
      <h2>数据源管理与监测</h2>
    </div>
      <el-tabs v-model="activeTab" class="function-tabs">
        <el-tab-pane label="多源数据集成" name="integration">
          <div class="tab-content">
            <!-- 数据源管理 -->
            <div class="integration-section">
              <el-form :model="integrationForm" label-width="120px" class="integration-form">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="数据源类型">
                      <el-select
                        v-model="integrationForm.sourceType"
                        placeholder="请选择数据源类型"
                        style="width: 100%"
                        @change="onSourceTypeChange"
                      >
                        <el-option label="社交媒体" value="social_media" />
                        <el-option label="电商" value="ecommerce" />
                        <el-option label="客服" value="customer_service" />
                        <el-option label="调研数据" value="survey" />
                        <el-option label="其他" value="other" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  
                  <el-col :span="12">
                    <el-form-item label="接入平台">
                      <el-select
                        v-model="integrationForm.platform"
                        :disabled="!integrationForm.sourceType"
                        placeholder="请选择具体平台"
                        style="width: 100%"
                      >
                        <el-option 
                          v-for="platform in platforms" 
                          :key="platform.value" 
                          :label="platform.label" 
                          :value="platform.value" 
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20">
                  <el-col :span="24">
                    <el-form-item label="API Key / 认证信息">
                      <el-input
                        v-model="integrationForm.apiKey"
                        type="password"
                        placeholder="请输入API Key或其他认证信息"
                        style="width: 100%"
                      />
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20" style="margin-top: 20px">
                  <el-col :span="8">
                    <el-button type="primary" @click="testConnection" style="width: 100%">
                      测试连接
                    </el-button>
                  </el-col>
                  <el-col :span="8">
                    <el-button type="success" @click="connectDataSource" style="width: 100%">
                      确认接入
                    </el-button>
                  </el-col>
                  <el-col :span="8">
                    <el-button @click="resetForm" style="width: 100%">
                      重置
                    </el-button>
                  </el-col>
                </el-row>
              </el-form>
            </div>
            
            <!-- 已连接数据源列表 -->
            <div class="connected-sources-section">
              <h3>已连接数据源</h3>
              <el-table :data="connectedSources" style="width: 100%">
                <el-table-column prop="name" label="数据源名称" width="180" />
                <el-table-column prop="type_name" label="类型" width="120" />
                <el-table-column prop="platform" label="平台" width="120" />
                <el-table-column prop="status" label="状态" width="100">
                  <template #default="{ row }">
                    <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
                      {{ row.status === 'active' ? '活跃' : '已断开' }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="lastSync" label="最后同步" width="180" />
                <el-table-column prop="dataCount" label="数据量" width="100" />
                <el-table-column label="操作" width="200">
                  <template #default="{ row }">
                    <el-button 
                      size="small" 
                      type="primary" 
                      @click="syncSource(row.id)"
                      :disabled="row.status !== 'active'"
                    >
                      立即同步
                    </el-button>
                    <el-button 
                      size="small" 
                      type="danger" 
                      @click="disconnectSource(row.id)"
                      :disabled="row.status !== 'active'"
                    >
                      断开连接
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="监测主题配置" name="monitoring">
          <div class="tab-content">
            <div class="monitoring-section">
              <el-form :model="monitoringForm" label-width="120px" class="monitoring-form">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="监测对象">
                      <el-select
                        v-model="monitoringForm.targetType"
                        placeholder="请选择监测对象"
                        style="width: 100%"
                      >
                        <el-option label="品牌" value="brand" />
                        <el-option label="产品" value="product" />
                        <el-option label="竞争对手" value="competitor" />
                        <el-option label="行业关键词" value="industry" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  
                  <el-col :span="12">
                    <el-form-item label="监测主题">
                      <el-input
                        v-model="monitoringForm.subject"
                        placeholder="请输入监测主题"
                        style="width: 100%"
                      />
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="时间范围">
                      <el-select
                        v-model="monitoringForm.timeRange"
                        placeholder="请选择时间范围"
                        style="width: 100%"
                      >
                        <el-option label="最近24小时" value="24h" />
                        <el-option label="最近7天" value="7d" />
                        <el-option label="最近30天" value="30d" />
                        <el-option label="自定义" value="custom" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  
                  <el-col :span="12">
                    <el-form-item label="数据来源">
                      <el-select
                        v-model="monitoringForm.dataSources"
                        multiple
                        placeholder="请选择数据来源"
                        style="width: 100%"
                      >
                        <el-option 
                          v-for="source in connectedSources" 
                          :key="source.id" 
                          :label="source.name" 
                          :value="source.id" 
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20">
                  <el-col :span="24">
                    <el-form-item label="关键词设置">
                      <el-input
                        v-model="monitoringForm.keywords"
                        type="textarea"
                        rows="3"
                        placeholder="请输入监测关键词，多个关键词用逗号分隔"
                        style="width: 100%"
                      />
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20" style="margin-top: 20px">
                  <el-col :span="8">
                    <el-button type="primary" @click="startMonitoring" style="width: 100%">
                      开始监测
                    </el-button>
                  </el-col>
                  <el-col :span="8">
                    <el-button @click="resetMonitoringForm" style="width: 100%">
                      重置
                    </el-button>
                  </el-col>
                </el-row>
              </el-form>
            </div>
            
            <!-- 监测主题列表 -->
            <div class="monitoring-topics-section">
              <h3>监测主题列表</h3>
              <el-table :data="monitoringTopics" style="width: 100%">
                <el-table-column prop="subject" label="监测主题" width="200" />
                <el-table-column prop="targetTypeName" label="监测对象" width="120" />
                <el-table-column prop="status" label="状态" width="100">
                  <template #default="{ row }">
                    <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
                      {{ row.status === 'active' ? '监测中' : '已停止' }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="startTime" label="开始时间" width="180" />
                <el-table-column prop="dataCount" label="数据量" width="100" />
                <el-table-column label="操作" width="200">
                  <template #default="{ row }">
                    <el-button 
                      size="small" 
                      type="primary" 
                      @click="toggleMonitoring(row.id)"
                    >
                      {{ row.status === 'active' ? '停止监测' : '开始监测' }}
                    </el-button>
                    <el-button 
                      size="small" 
                      type="danger" 
                      @click="removeMonitoring(row.id)"
                    >
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="数据质量分析" name="quality">
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
                  <el-table-column prop="type" label="问题类型" width="120" />
                  <el-table-column prop="description" label="问题描述" />
                  <el-table-column prop="severity" label="严重程度" width="100">
                    <template #default="{ row }">
                      <el-tag :type="row.severity === '高' ? 'danger' : row.severity === '中' ? 'warning' : 'info'">
                        {{ row.severity }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="count" label="数量" width="80" />
                  <el-table-column prop="status" label="状态" width="100">
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
        </el-tab-pane>
        
        <el-tab-pane label="实时监控仪表盘" name="dashboard">
          <div class="tab-content">
            <div class="dashboard-section">
              <h3>实时监控仪表盘</h3>
              <div class="dashboard-stats">
                <div class="stat-card">
                  <div class="stat-icon"><mdicon name="data-table-outline-rounded" size="50" color="var(--color-info)"/></div>
                  <div class="stat-content">
                    <div class="stat-value">{{ dashboardStats.totalData }}</div>
                    <div class="stat-label">总数据量</div>
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-icon"><mdicon name="fiber-new-rounded" size="50" color="var(--color-info)"/></div>
                  <div class="stat-content">
                    <div class="stat-value">{{ dashboardStats.todayData }}</div>
                    <div class="stat-label">今日新增</div>
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-icon"><mdicon name="heart-smile-outline-rounded" size="50" color="var(--color-info)"/></div>
                  <div class="stat-content">
                    <div class="stat-value">{{ dashboardStats.positiveRate }}%</div>
                    <div class="stat-label">正面情感率</div>
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-icon"><mdicon name="bookmark-check-outline-rounded" size="50" color="var(--color-info)"/></div>
                  <div class="stat-content">
                    <div class="stat-value">{{ dashboardStats.topicCount }}</div>
                    <div class="stat-label">监测主题数</div>
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-icon"><mdicon name="star-rate-rounded" size="50" color="var(--color-info)"/></div>
                  <div class="stat-content">
                    <div class="stat-value">{{ dashboardStats.qualityScore }}</div>
                    <div class="stat-label">数据质量评分</div>
                  </div>
                </div>
              </div>
              
              <!-- 热点话题聚类 -->
              <div class="topic-clusters">
                <h3>热点话题聚类</h3>
                <el-table :data="topicClusters" style="width: 100%">
                  <el-table-column prop="rank" label="排名" width="80" />
                  <el-table-column prop="name" label="话题名称" width="200" />
                  <el-table-column prop="mentionCount" label="提及次数" width="120" />
                  <el-table-column prop="sentiment" label="情感倾向" width="100">
                    <template #default="{ row }">
                      <el-tag :type="row.sentiment === '正面' ? 'success' : row.sentiment === '负面' ? 'danger' : 'info'">
                        {{ row.sentiment }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="trend" label="趋势" width="100">
                    <template #default="{ row }">
                      <span :style="{ color: row.trend === '上升' ? 'green' : row.trend === '下降' ? 'red' : 'orange' }">
                        {{ row.trend === '上升' ? '上升' : row.trend === '下降' ? '下降' : '平稳' }}
                      </span>
                    </template>
                  </el-table-column>
                  <el-table-column prop="duration" label="持续时间" width="120" />
                </el-table>
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
import { ElMessage } from 'element-plus'

// 响应式数据
const activeTab = ref('integration')

// 集成表单
const integrationForm = ref({
  sourceType: '',
  platform: '',
  apiKey: ''
})

// 监测表单
const monitoringForm = ref({
  targetType: '',
  subject: '',
  timeRange: '24h',
  dataSources: [],
  keywords: ''
})

// 平台列表
const platforms = ref([
  { label: '微博', value: 'weibo' },
  { label: '抖音', value: 'douyin' },
  { label: '天猫', value: 'tmall' },
  { label: '京东', value: 'jd' }
])

// 已连接数据源
const connectedSources = ref([
  {
    id: 1,
    name: '微博',
    type: 'social_media',
    type_name: '社交媒体',
    platform: '微博',
    status: 'active',
    lastSync: '2026-02-03 10:25',
    dataCount: 12450,
    createTime: '2023-11-15',
    description: '官方API接入'
  },
  {
    id: 2,
    name: '美团H5',
    type: 'social_media',
    type_name: '电商',
    platform: '美团外卖',
    status: 'active',
    lastSync: '2026-02-03 10:25',
    dataCount: 8760,
    createTime: '2023-11-20',
    description: '关键词监控'
  },
  {
    id: 2,
    name: '小红书',
    type: 'social_media',
    type_name: '社交平台',
    platform: '小红书',
    status: 'active',
    lastSync: '2026-02-03 10:25',
    dataCount: 8760,
    createTime: '2023-11-20',
    description: '关键词监控'
  }
])

// 监测主题
const monitoringTopics = ref([
  {
    id: 1,
    subject: '品牌声誉',
    targetType: 'brand',
    targetTypeName: '品牌',
    status: 'active',
    startTime: '2026-02-03 09:00',
    dataCount: 23,
    dataSources: [1, 2],
    keywords: '品牌, 声誉, 形象'
  },
  {
    id: 2,
    subject: '新产品体验',
    targetType: 'product',
    targetTypeName: '产品',
    status: 'active',
    startTime: '2026-02-02 14:30',
    dataCount: 8,
    dataSources: [1],
    keywords: '新产品, 体验, 功能'
  }
])

// 数据质量指标
const qualityMetrics = ref({
  completeness: 78,
  accuracy: 74,
  timeliness: 84,
  consistency: 82,
  validity: 74
})

// 数据质量问题
const qualityIssues = ref([
  { type: '数据缺失', description: '部分字段为空值', severity: '中', count: 24, status: '待处理' },
  { type: '重复数据', description: '存在相同内容的重复记录', severity: '低', count: 15, status: '已处理' },
  { type: '格式错误', description: '某些字段格式不规范', severity: '高', count: 8, status: '待处理' },
  { type: '时间错误', description: '部分数据时间戳异常', severity: '中', count: 12, status: '处理中' }
])

// 仪表盘统计
const dashboardStats = ref({
  totalData: 1783,
  todayData: 874,
  positiveRate: 72.3,
  positiveChange: 3.2,
  topicCount: 2,
  trendingTopic: '#新产品体验#',
  qualityScore: 82,
  qualityTrend: 2
})

// 话题聚类
const topicClusters = ref([
  { rank: 1, name: '新产品体验', mentionCount: 13, sentiment: '正面', trend: '上升', duration: '3天' },
  { rank: 2, name: '物流服务', mentionCount: 5, sentiment: '中性', trend: '平稳', duration: '持续' },
  { rank: 3, name: '价格策略', mentionCount: 3, sentiment: '负面', trend: '下降', duration: '5天' },
  { rank: 4, name: '售后服务', mentionCount: 20, sentiment: '正面', trend: '上升', duration: '2天' },
  { rank: 5, name: '品牌声誉', mentionCount: 47, sentiment: '正面', trend: '平稳', duration: '持续' }
])

// 方法
const onSourceTypeChange = () => {
  // 重置平台选择
  integrationForm.value.platform = ''
  // 这里可以根据数据源类型动态获取平台列表
}

const testConnection = async () => {
  if (!integrationForm.value.sourceType || !integrationForm.value.platform) {
    ElMessage.warning('请选择数据源类型和平台')
    return
  }
  
  // 模拟测试连接
  ElMessage.success('连接测试成功！')
}

const connectDataSource = async () => {
  if (!integrationForm.value.sourceType || !integrationForm.value.platform) {
    ElMessage.warning('请选择数据源类型和平台')
    return
  }
  
  // 模拟连接数据源
  const newSource = {
    id: connectedSources.value.length + 1,
    name: `${integrationForm.value.platform}接入`,
    type: integrationForm.value.sourceType,
    type_name: integrationForm.value.sourceType === 'social_media' ? '社交媒体' : '电商',
    platform: integrationForm.value.platform,
    status: 'active',
    lastSync: new Date().toLocaleString(),
    dataCount: 0,
    createTime: new Date().toLocaleDateString(),
    description: '新接入数据源'
  }
  
  connectedSources.value.push(newSource)
  ElMessage.success('数据源连接成功！')
  resetForm()
}

const resetForm = () => {
  integrationForm.value = {
    sourceType: '',
    platform: '',
    apiKey: ''
  }
}

const syncSource = async (sourceId) => {
  // 模拟同步数据源
  const source = connectedSources.value.find(s => s.id === sourceId)
  if (source) {
    source.lastSync = new Date().toLocaleString()
    source.dataCount += Math.floor(Math.random() * 100) + 50
    ElMessage.success('数据源同步成功！')
  }
}

const disconnectSource = async (sourceId) => {
  // 模拟断开数据源
  const source = connectedSources.value.find(s => s.id === sourceId)
  if (source) {
    source.status = 'inactive'
    ElMessage.success('数据源已断开连接！')
  }
}

const startMonitoring = async () => {
  if (!monitoringForm.value.targetType || !monitoringForm.value.subject) {
    ElMessage.warning('请选择监测对象并输入监测主题')
    return
  }
  
  // 模拟开始监测
  const newTopic = {
    id: monitoringTopics.value.length + 1,
    subject: monitoringForm.value.subject,
    targetType: monitoringForm.value.targetType,
    targetTypeName: monitoringForm.value.targetType === 'brand' ? '品牌' : monitoringForm.value.targetType === 'product' ? '产品' : '其他',
    status: 'active',
    startTime: new Date().toLocaleString(),
    dataCount: 0,
    dataSources: monitoringForm.value.dataSources,
    keywords: monitoringForm.value.keywords
  }
  
  monitoringTopics.value.push(newTopic)
  ElMessage.success('监测主题已启动！')
  resetMonitoringForm()
}

const resetMonitoringForm = () => {
  monitoringForm.value = {
    targetType: '',
    subject: '',
    timeRange: '24h',
    dataSources: [],
    keywords: ''
  }
}

const toggleMonitoring = async (topicId) => {
  // 模拟切换监测状态
  const topic = monitoringTopics.value.find(t => t.id === topicId)
  if (topic) {
    topic.status = topic.status === 'active' ? 'inactive' : 'active'
    ElMessage.success(`监测主题已${topic.status === 'active' ? '启动' : '停止'}！`)
  }
}

const removeMonitoring = async (topicId) => {
  // 模拟删除监测主题
  const index = monitoringTopics.value.findIndex(t => t.id === topicId)
  if (index !== -1) {
    monitoringTopics.value.splice(index, 1)
    ElMessage.success('监测主题已删除！')
  }
}

const getQualityColor = (value) => {
  if (value >= 90) return '#52c41a'
  if (value >= 70) return '#73d13d'
  if (value >= 50) return '#ffd666'
  return '#ff7875'
}

// 生命周期
onMounted(() => {
  console.log('数据源管理组件已挂载')
})
</script>

<style scoped>
.data-source-container {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: 100vh;
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

.integration-section,
.monitoring-section,
.quality-section,
.dashboard-section {
  margin-bottom: 30px;
}

.integration-section h3,
.monitoring-section h3,
.quality-section h3,
.dashboard-section h3 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 2px solid var(--color-primary-hover);
  padding-bottom: 10px;
}

.integration-form,
.monitoring-form {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.connected-sources-section,
.monitoring-topics-section {
  margin-top: 30px;
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

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  align-items: center;
}

.stat-icon {
  font-size: 32px;
  margin-right: 20px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 5px;
}

.quality-issues,
.topic-clusters {
  margin-top: 30px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .quality-metrics,
  .dashboard-stats {
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