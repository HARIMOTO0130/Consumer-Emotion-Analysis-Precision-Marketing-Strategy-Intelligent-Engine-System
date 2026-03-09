<template>
  <div class="pos-data-visualization">
    <!-- 数据导入区域 -->
    <div class="data-import-section">
      <el-card class="import-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="header-title">
              <mdicon name="database-import" size="28"/>
              <h3>POS数据导入</h3>
            </div>
          </div>
        </template>
        
        <!-- 数据源选择 -->
        <div class="data-source-selector">
          <el-radio-group v-model="dataSource" @change="handleDataSourceChange">
            <el-radio label="odoo">Odoo 19系统</el-radio>
            <el-radio label="csv">CSV文件导入</el-radio>
          </el-radio-group>
        </div>

        <!-- Odoo配置表单 -->
        <div v-if="dataSource === 'odoo'" class="odoo-config-form">
          <el-form :model="odooConfig" :rules="odooRules" ref="odooForm" label-width="120px">
            <el-form-item label="服务器地址" prop="host">
              <el-input v-model="odooConfig.host" placeholder="https://your-odoo-instance.com" />
            </el-form-item>
            <el-form-item label="数据库名称" prop="database">
              <el-input v-model="odooConfig.database" placeholder="your-database" />
            </el-form-item>
            <el-form-item label="用户名" prop="username">
              <el-input v-model="odooConfig.username" placeholder="admin" />
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input v-model="odooConfig.password" type="password" placeholder="请输入密码" />
            </el-form-item>
            <el-form-item label="查询选项">
              <div class="query-options">
                <el-date-picker
                  v-model="odooConfig.dateRange"
                  type="daterange"
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  format="YYYY-MM-DD"
                  value-format="YYYY-MM-DD"
                />
                <el-input-number
                  v-model="odooConfig.limit"
                  :min="1"
                  :max="10000"
                  label="记录数量限制"
                  style="margin-left: 10px;"
                />
              </div>
            </el-form-item>
            <el-form-item>
              <el-button 
                type="primary" 
                @click="connectToOdoo" 
                :loading="loading"
                :disabled="!canConnect"
              >
                <mdicon name="connection" size="18" v-if="!loading"/>
                <span>{{ loading ? '连接中...' : '连接Odoo' }}</span>
              </el-button>
              <el-button @click="testConnection" :loading="testingConnection">测试连接</el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- CSV导入表单 -->
        <div v-if="dataSource === 'csv'" class="csv-import-form">
          <div class="file-upload-area">
            <el-upload
              drag
              :auto-upload="false"
              :show-file-list="true"
              :on-change="handleFileChange"
              :on-remove="handleFileRemove"
              accept=".csv"
              multiple
              :limit="1"
            >
              <mdicon name="upload" size="50" color="#c0c4cc"/>
              <div class="el-upload__text">
                将CSV文件拖到此处，或<em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  仅支持CSV格式文件，建议文件大小不超过10MB
                </div>
              </template>
            </el-upload>
          </div>

          <!-- 字段映射配置 -->
          <div v-if="csvFile && csvHeaders.length > 0" class="field-mapping-section">
            <h4>字段映射配置</h4>
            <div class="mapping-table">
              <el-table :data="mappingFields" style="width: 100%">
                <el-table-column prop="required" label="必需" width="80">
                  <template #default="{ row }">
                    <el-tag v-if="row.required" type="danger" size="small">必需</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="name" label="系统字段" width="120">
                  <template #default="{ row }">
                    <span class="field-name">{{ row.name }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="description" label="描述" width="200">
                  <template #default="{ row }">
                    <span class="field-desc">{{ row.description }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="CSV字段映射">
                  <template #default="{ row }">
                    <el-select 
                      v-model="fieldMapping[row.key]" 
                      placeholder="选择对应字段"
                      :disabled="!row.required && !fieldMapping[row.key]"
                    >
                      <el-option
                        v-for="header in csvHeaders"
                        :key="header"
                        :label="header"
                        :value="header"
                      />
                    </el-select>
                  </template>
                </el-table-column>
              </el-table>
            </div>

            <!-- 预览数据 -->
            <div v-if="csvPreview.length > 0" class="data-preview">
              <h4>数据预览</h4>
              <el-table :data="csvPreview" style="width: 100%" height="200">
                <el-table-column 
                  v-for="header in csvHeaders.slice(0, 8)" 
                  :key="header" 
                  :prop="header" 
                  :label="header" 
                  width="120"
                />
              </el-table>
            </div>

            <!-- 验证和导入按钮 -->
            <div class="mapping-actions">
              <el-button 
                type="primary" 
                @click="validateMapping" 
                :disabled="!canValidate"
              >
                验证映射
              </el-button>
              <el-button 
                type="success" 
                @click="importCSVData" 
                :loading="loading"
                :disabled="!canImport"
              >
                导入数据
              </el-button>
              <el-button @click="resetMapping">重置映射</el-button>
            </div>

            <!-- 验证结果 -->
            <div v-if="mappingValidation" class="validation-result">
              <el-alert
                :title="mappingValidation.title"
                :type="mappingValidation.type"
                :description="mappingValidation.description"
                show-icon
                :closable="false"
              />
            </div>
          </div>
        </div>

        <!-- 数据状态显示 -->
        <div class="data-status">
          <el-alert
            v-if="dataStatus.hasData"
            title="数据已加载"
            type="success"
            :description="`数据源: ${dataStatus.metadata?.sourceSystem || '未知'} | 记录数: ${dataStatus.metadata?.totalRecords || 0} | 日期范围: ${dataStatus.metadata?.dateRange?.start || 'N/A'} 至 ${dataStatus.metadata?.dateRange?.end || 'N/A'}`"
            show-icon
            :closable="false"
          />
          <el-alert
            v-else-if="dataStatus.error"
            title="数据加载失败"
            type="error"
            :description="dataStatus.error"
            show-icon
            :closable="false"
          />
        </div>
      </el-card>
    </div>

    <!-- 数据可视化区域 -->
    <div v-if="dataStatus.hasData" class="visualization-section">
      <div class="charts-grid">
        <!-- 销售趋势图 -->
        <el-card class="chart-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <div class="header-title">
                <mdicon name="trending-up" size="24"/>
                <h4>销售趋势分析</h4>
              </div>
              <div class="chart-controls">
                <el-select v-model="timeRange" @change="updateCharts" size="small">
                  <el-option label="日度" value="daily"/>
                  <el-option label="周度" value="weekly"/>
                  <el-option label="月度" value="monthly"/>
                </el-select>
              </div>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="salesTrendOption" autoresize />
          </div>
        </el-card>

        <!-- 销售额分布饼图 -->
        <el-card class="chart-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <div class="header-title">
                <mdicon name="pie-chart" size="24"/>
                <h4>销售额分布</h4>
              </div>
              <div class="chart-controls">
                <el-select v-model="pieChartType" @change="updateCharts" size="small">
                  <el-option label="按产品类别" value="category"/>
                  <el-option label="按产品" value="product"/>
                  <el-option label="按客户类型" value="customer_type"/>
                </el-select>
              </div>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="salesDistributionOption" autoresize />
          </div>
        </el-card>

        <!-- 销售额对比柱状图 -->
        <el-card class="chart-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <div class="header-title">
                <mdicon name="chart-bar" size="24"/>
                <h4>销售额对比</h4>
              </div>
              <div class="chart-controls">
                <el-select v-model="barChartType" @change="updateCharts" size="small">
                  <el-option label="按产品类别" value="category"/>
                  <el-option label="按产品" value="product"/>
                  <el-option label="按客户类型" value="customer_type"/>
                </el-select>
              </div>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="salesComparisonOption" autoresize />
          </div>
        </el-card>

        <!-- 数据概览卡片 -->
        <div class="overview-cards">
          <div class="overview-card">
            <div class="card-icon"><mdicon name="currency-usd" size="32" color="#52c41a"/></div>
            <div class="card-content">
              <div class="card-value">{{ formatCurrency(overviewStats.totalSales) }}</div>
              <div class="card-label">总销售额</div>
            </div>
          </div>
          <div class="overview-card">
            <div class="card-icon"><mdicon name="package-variant" size="32" color="#1890ff"/></div>
            <div class="card-content">
              <div class="card-value">{{ overviewStats.totalQuantity.toLocaleString() }}</div>
              <div class="card-label">总销售量</div>
            </div>
          </div>
          <div class="overview-card">
            <div class="card-icon"><mdicon name="calendar-today" size="32" color="#fa8c16"/></div>
            <div class="card-content">
              <div class="card-value">{{ overviewStats.avgDailySales.toLocaleString() }}</div>
              <div class="card-label">日均销售额</div>
            </div>
          </div>
          <div class="overview-card">
            <div class="card-icon"><mdicon name="store" size="32" color="#722ed1"/></div>
            <div class="card-content">
              <div class="card-value">{{ overviewStats.uniqueProducts }}</div>
              <div class="card-label">产品种类数</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { ElCard, ElForm, ElFormItem, ElInput, ElInputNumber, ElSelect, ElOption, ElButton, ElUpload, ElTable, ElTableColumn, ElTag, ElAlert, ElRadioGroup, ElRadio, ElDatePicker } from 'element-plus'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart, BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent, TitleComponent } from 'echarts/components'
import posDataService from '../services/posDataService'
import { formatDate } from '../utils/time-format'

// 注册ECharts组件
use([
  CanvasRenderer,
  LineChart,
  PieChart,
  BarChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent
])

// 响应式数据
const dataSource = ref('odoo')
const loading = ref(false)
const testingConnection = ref(false)

// Odoo配置
const odooConfig = reactive({
  host: '',
  database: '',
  username: '',
  password: '',
  dateRange: [],
  limit: 1000
})

const odooRules = {
  host: [{ required: true, message: '请输入服务器地址', trigger: 'blur' }],
  database: [{ required: true, message: '请输入数据库名称', trigger: 'blur' }],
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

// CSV导入相关
const csvFile = ref(null)
const csvHeaders = ref([])
const csvPreview = ref([])
const fieldMapping = ref({})
const mappingValidation = ref(null)

// 数据状态
const dataStatus = computed(() => posDataService.getStatus())

// 图表配置
const timeRange = ref('daily')
const pieChartType = ref('category')
const barChartType = ref('category')

// 字段映射配置
const mappingFields = ref([
  { key: 'date', name: '日期', description: '销售日期', required: true },
  { key: 'product', name: '产品', description: '产品名称', required: true },
  { key: 'category', name: '类别', description: '产品类别', required: false },
  { key: 'sales', name: '销售额', description: '销售金额', required: true },
  { key: 'quantity', name: '数量', description: '销售数量', required: true },
  { key: 'customer_type', name: '客户类型', description: '客户分类', required: false },
  { key: 'customer_name', name: '客户名称', description: '客户姓名', required: false },
  { key: 'order_id', name: '订单ID', description: '订单标识', required: false }
])

// 计算属性
const canConnect = computed(() => {
  return odooConfig.host && odooConfig.database && odooConfig.username && odooConfig.password
})

const canValidate = computed(() => {
  return csvFile.value && csvHeaders.value.length > 0 && Object.keys(fieldMapping.value).length > 0
})

const canImport = computed(() => {
  return canValidate.value && mappingValidation.value && mappingValidation.value.type === 'success'
})

// 图表选项
const salesTrendOption = computed(() => {
  if (!dataStatus.value.hasData) return {}
  
  const timeSeries = posDataService.getTimeSeriesData(posDataService.data, timeRange.value)
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['销售额', '销售量'],
      top: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: timeSeries.dates,
      axisPointer: { type: 'shadow' }
    },
    yAxis: [
      {
        type: 'value',
        name: '销售额',
        position: 'left',
        axisLabel: { formatter: '{value} 元' }
      },
      {
        type: 'value',
        name: '销售量',
        position: 'right',
        axisLabel: { formatter: '{value} 件' }
      }
    ],
    series: [
      {
        name: '销售额',
        type: 'line',
        smooth: true,
        data: timeSeries.sales,
        itemStyle: { color: '#52c41a' },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(82, 196, 26, 0.3)' },
              { offset: 1, color: 'rgba(82, 196, 26, 0.05)' }
            ]
          }
        }
      },
      {
        name: '销售量',
        type: 'bar',
        yAxisIndex: 1,
        data: timeSeries.quantity,
        itemStyle: { color: '#1890ff' }
      }
    ]
  }
})

const salesDistributionOption = computed(() => {
  if (!dataStatus.value.hasData) return {}
  
  const pieData = posDataService.getPieChartData(posDataService.data, pieChartType.value)
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: pieData.map(item => item.name)
    },
    series: [
      {
        name: '销售额分布',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}: {d}%'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: pieData
      }
    ]
  }
})

const salesComparisonOption = computed(() => {
  if (!dataStatus.value.hasData) return {}
  
  const barData = posDataService.getBarChartData(posDataService.data, barChartType.value)
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    legend: {
      data: ['销售额', '销售量'],
      top: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: barData.categories,
      axisPointer: { type: 'shadow' }
    },
    yAxis: [
      {
        type: 'value',
        name: '销售额',
        position: 'left',
        axisLabel: { formatter: '{value} 元' }
      },
      {
        type: 'value',
        name: '销售量',
        position: 'right',
        axisLabel: { formatter: '{value} 件' }
      }
    ],
    series: [
      {
        name: '销售额',
        type: 'bar',
        data: barData.sales,
        itemStyle: { color: '#52c41a' }
      },
      {
        name: '销售量',
        type: 'bar',
        yAxisIndex: 1,
        data: barData.quantity,
        itemStyle: { color: '#1890ff' }
      }
    ]
  }
})

const overviewStats = computed(() => {
  if (!dataStatus.value.hasData) {
    return {
      totalSales: 0,
      totalQuantity: 0,
      avgDailySales: 0,
      uniqueProducts: 0
    }
  }
  
  const aggregation = posDataService.getSalesAggregation(posDataService.data)
  const dateRange = posDataService.data.metadata.dateRange
  const days = dateRange.start && dateRange.end ? 
    Math.ceil((new Date(dateRange.end) - new Date(dateRange.start)) / (1000 * 60 * 60 * 24)) + 1 : 1
  
  return {
    totalSales: aggregation.totalSales,
    totalQuantity: aggregation.totalQuantity,
    avgDailySales: Math.round(aggregation.totalSales / days),
    uniqueProducts: posDataService.data.metadata.products.length
  }
})

// 方法
const handleDataSourceChange = (value) => {
  if (value === 'csv') {
    // 重置CSV相关状态
    csvFile.value = null
    csvHeaders.value = []
    csvPreview.value = []
    fieldMapping.value = {}
    mappingValidation.value = null
  }
}

const connectToOdoo = async () => {
  if (!canConnect.value) return
  
  loading.value = true
  try {
    const options = {
      domain: [],
      fields: ['id', 'date_order', 'amount_total', 'lines', 'partner_id', 'session_id'],
      limit: odooConfig.limit
    }
    
    if (odooConfig.dateRange && odooConfig.dateRange.length === 2) {
      options.domain = [
        ['date_order', '>=', odooConfig.dateRange[0]],
        ['date_order', '<=', odooConfig.dateRange[1]]
      ]
    }
    
    await posDataService.fetchFromOdoo(odooConfig, options)
    ElMessage.success('Odoo数据加载成功')
  } catch (error) {
    ElMessage.error(`连接失败: ${error.message}`)
  } finally {
    loading.value = false
  }
}

const testConnection = async () => {
  if (!canConnect.value) return
  
  testingConnection.value = true
  try {
    // 简单的连接测试
    const response = await fetch(`${odooConfig.host}/web`, { method: 'HEAD' })
    if (response.ok) {
      ElMessage.success('连接测试成功')
    } else {
      ElMessage.error('连接测试失败')
    }
  } catch (error) {
    ElMessage.error(`连接测试失败: ${error.message}`)
  } finally {
    testingConnection.value = false
  }
}

const handleFileChange = (file, fileList) => {
  csvFile.value = file.raw
  parseCSVHeaders(file.raw)
}

const handleFileRemove = () => {
  csvFile.value = null
  csvHeaders.value = []
  csvPreview.value = []
  fieldMapping.value = {}
  mappingValidation.value = null
}

const parseCSVHeaders = async (file) => {
  try {
    const text = await posDataService.readFileAsText(file)
    const lines = text.split('\n').filter(line => line.trim())
    if (lines.length < 2) {
      throw new Error('CSV文件内容为空或格式不正确')
    }
    
    // 解析表头
    const headers = lines[0].split(',').map(h => h.trim())
    csvHeaders.value = headers
    
    // 生成预览数据
    const previewData = []
    for (let i = 1; i < Math.min(lines.length, 6); i++) {
      const values = lines[i].split(',').map(v => v.trim())
      const row = {}
      headers.forEach((header, index) => {
        row[header] = values[index] || ''
      })
      previewData.push(row)
    }
    csvPreview.value = previewData
    
    // 设置默认映射
    resetMapping()
    
  } catch (error) {
    ElMessage.error(`解析CSV文件失败: ${error.message}`)
  }
}

const resetMapping = () => {
  const defaultMapping = posDataService.getDefaultMapping()
  fieldMapping.value = { ...defaultMapping }
}

const validateMapping = () => {
  const result = posDataService.validateMapping(fieldMapping.value, csvHeaders.value)
  
  if (result.valid) {
    mappingValidation.value = {
      type: 'success',
      title: '映射验证成功',
      description: '所有必需字段都已正确映射'
    }
  } else {
    mappingValidation.value = {
      type: 'error',
      title: '映射验证失败',
      description: result.errors.join('; ')
    }
  }
}

const importCSVData = async () => {
  if (!canImport.value) return
  
  loading.value = true
  try {
    await posDataService.importCSV(csvFile.value, fieldMapping.value)
    ElMessage.success('CSV数据导入成功')
  } catch (error) {
    ElMessage.error(`数据导入失败: ${error.message}`)
  } finally {
    loading.value = false
  }
}

const updateCharts = () => {
  // 图表会自动更新，因为使用了computed属性
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}

// 生命周期
onMounted(() => {
  // 初始化默认映射
  resetMapping()
})
</script>

<style scoped>
.pos-data-visualization {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.data-import-section {
  margin-bottom: 30px;
}

.import-card {
  border-radius: 12px;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-title h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: #2c3e50;
}

.data-source-selector {
  margin-bottom: 20px;
  padding: 15px;
  background-color: rgba(24, 144, 255, 0.05);
  border-radius: 8px;
}

.odoo-config-form {
  padding: 10px;
}

.query-options {
  display: flex;
  gap: 10px;
  align-items: center;
}

.csv-import-form {
  padding: 10px;
}

.file-upload-area {
  margin-bottom: 20px;
}

.field-mapping-section {
  margin-top: 20px;
  padding: 15px;
  background-color: #fafafa;
  border-radius: 8px;
}

.field-mapping-section h4 {
  margin: 0 0 15px 0;
  color: #333;
}

.mapping-table {
  margin-bottom: 20px;
}

.field-name {
  font-weight: 600;
  color: #2c3e50;
}

.field-desc {
  color: #666;
  font-size: 12px;
}

.data-preview {
  margin: 20px 0;
}

.data-preview h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.mapping-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.validation-result {
  margin-top: 10px;
}

.data-status {
  margin-top: 20px;
}

.visualization-section {
  margin-top: 30px;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.chart-card {
  border-radius: 12px;
  overflow: hidden;
}

.chart-card .header-title h4 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #2c3e50;
}

.chart-controls {
  display: flex;
  gap: 10px;
}

.chart-container {
  height: 400px;
  padding: 10px;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 20px;
}

.overview-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 15px;
  transition: all 0.3s ease;
}

.overview-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-content {
  flex: 1;
}

.card-value {
  font-size: 24px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 4px;
}

.card-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    height: 300px;
  }
  
  .overview-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .query-options {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>