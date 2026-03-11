<template>
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
        <el-table-column prop="name" label="数据源名称"   />
        <el-table-column prop="type_name" label="类型"   />
        <el-table-column prop="platform" label="平台"   />
        <el-table-column prop="status" label="状态"  >
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '活跃' : '已断开' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="lastSync" label="最后同步"   />
        <el-table-column prop="dataCount" label="数据量"   />
        <el-table-column label="操作"  >
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
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { ElForm, ElFormItem, ElSelect, ElOption, ElInput, ElButton, ElTable, ElTableColumn, ElTag, ElRow, ElCol } from 'element-plus'

const props = defineProps({
  integrationForm: {
    type: Object,
    required: true
  },
  platforms: {
    type: Array,
    required: true
  },
  connectedSources: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['source-type-change', 'test-connection', 'connect-data-source', 'reset-form', 'sync-source', 'disconnect-source'])

const onSourceTypeChange = (value) => {
  emit('source-type-change', value)
}

const testConnection = () => {
  emit('test-connection')
}

const connectDataSource = () => {
  emit('connect-data-source')
}

const resetForm = () => {
  emit('reset-form')
}

const syncSource = (sourceId) => {
  emit('sync-source', sourceId)
}

const disconnectSource = (sourceId) => {
  emit('disconnect-source', sourceId)
}
</script>

<style scoped>
.integration-section h3,
.connected-sources-section h3 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 2px solid var(--color-primary-hover);
  padding-bottom: 10px;
}

.integration-form {
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