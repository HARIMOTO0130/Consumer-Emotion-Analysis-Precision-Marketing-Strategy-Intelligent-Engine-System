<template>
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
        <el-table-column prop="subject" label="监测主题"   />
        <el-table-column prop="targetTypeName" label="监测对象"   />
        <el-table-column prop="status" label="状态"  >
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '监测中' : '已停止' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="startTime" label="开始时间"   />
        <el-table-column prop="dataCount" label="数据量"   />
        <el-table-column label="操作"  >
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
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { ElForm, ElFormItem, ElSelect, ElOption, ElInput, ElButton, ElTable, ElTableColumn, ElTag, ElRow, ElCol } from 'element-plus'

const props = defineProps({
  monitoringForm: {
    type: Object,
    required: true
  },
  connectedSources: {
    type: Array,
    required: true
  },
  monitoringTopics: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['start-monitoring', 'reset-monitoring-form', 'toggle-monitoring', 'remove-monitoring'])

const startMonitoring = () => {
  emit('start-monitoring')
}

const resetMonitoringForm = () => {
  emit('reset-monitoring-form')
}

const toggleMonitoring = (topicId) => {
  emit('toggle-monitoring', topicId)
}

const removeMonitoring = (topicId) => {
  emit('remove-monitoring', topicId)
}
</script>

<style scoped>
.monitoring-section h3,
.monitoring-topics-section h3 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 2px solid var(--color-primary-hover);
  padding-bottom: 10px;
}

.monitoring-form {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .el-row {
    flex-direction: column;
  }
  
  .el-col {
    width: 100% !important;
    margin-bottom: 15px;
  }
}
</style>