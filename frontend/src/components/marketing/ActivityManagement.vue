<template>
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
        <el-table-column prop="name" label="活动名称"   />
        <el-table-column prop="type" label="活动类型"  >
          <template #default="{ row }">
            <el-tag :type="getTypeColor(row.type)">
              {{ getTypeName(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="startTime" label="开始时间"   />
        <el-table-column prop="endTime" label="结束时间"   />
        <el-table-column prop="status" label="状态"  >
          <template #default="{ row }">
            <el-tag :type="getStatusColor(row.status)">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="budget" label="预算"   />
        <el-table-column prop="participants" label="参与人数"   />
        <el-table-column label="操作"  >
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
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { ElForm, ElFormItem, ElInput, ElSelect, ElOption, ElDatePicker, ElButton, ElTable, ElTableColumn, ElTag, ElRow, ElCol } from 'element-plus'

const props = defineProps({
  activityForm: {
    type: Object,
    required: true
  },
  marketingActivities: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['create-activity', 'reset-activity-form', 'view-activity-detail', 'cancel-activity'])

const createActivity = () => {
  emit('create-activity')
}

const resetActivityForm = () => {
  emit('reset-activity-form')
}

const viewActivityDetail = (activityId) => {
  emit('view-activity-detail', activityId)
}

const cancelActivity = (activityId) => {
  emit('cancel-activity', activityId)
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
</script>

<style scoped>
.activity-create h3,
.activity-list-section h3 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 2px solid var(--color-primary-hover);
  padding-bottom: 10px;
}

.activity-form {
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