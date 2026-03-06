<template>
  <div class="tab-content">
    <!-- 活动创建表单 -->
    <div class="activity-create">
      <h3>创建营销活动</h3>
      <el-form :model="activityForm" label-width="120px" class="activity-form">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="活动名称">
              <el-input v-model="activityForm.name" placeholder="请输入活动名称" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="活动类型">
              <el-select v-model="activityForm.type" placeholder="请选择活动类型" style="width: 100%">
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
              <el-date-picker v-model="activityForm.startTime" type="datetime" placeholder="选择开始时间" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束时间">
              <el-date-picker v-model="activityForm.endTime" type="datetime" placeholder="选择结束时间" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="预算">
              <el-input v-model="activityForm.budget" type="number" placeholder="请输入预算" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="目标受众">
              <el-select v-model="activityForm.audience" placeholder="请选择目标受众" style="width: 100%">
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
              <el-input v-model="activityForm.description" type="textarea" rows="3" placeholder="请输入活动描述" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="margin-top: 20px">
          <el-col :span="8">
            <el-button type="primary" @click="createActivity" style="width: 100%">创建活动</el-button>
          </el-col>
          <el-col :span="8">
            <el-button @click="resetActivityForm" style="width: 100%">重置</el-button>
          </el-col>
        </el-row>
      </el-form>
    </div>

    <!-- 活动列表 -->
    <div class="activity-list-section">
      <h3>营销活动列表</h3>
      <el-table :data="marketingActivities" style="width: 100%">
        <el-table-column prop="name" label="活动名称" />
        <el-table-column prop="type" label="活动类型">
          <template #default="{ row }">
            <el-tag :type="getTypeColor(row.type)">{{ getTypeName(row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="startTime" label="开始时间" />
        <el-table-column prop="endTime" label="结束时间" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusColor(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="budget" label="预算" />
        <el-table-column prop="participants" label="参与人数" />
        <el-table-column label="操作">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="viewActivityDetail(row.id)">查看详情</el-button>
            <el-button size="small" type="danger" @click="cancelActivity(row.id)" :disabled="row.status === '已结束' || row.status === '已取消'">取消活动</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const activityForm = ref({
  name: '',
  type: '',
  startTime: '',
  endTime: '',
  budget: '',
  audience: '',
  description: ''
})

const marketingActivities = ref([
  {
    id: 1,
    name: '双11促销活动',
    type: 'promotion',
    startTime: '2025-11-11 00:00:00',
    endTime: '2025-11-11 23:59:59',
    status: '已结束',
    budget: '3万',
    participants: '240'
  },
  // ... 其余数据
  {
    id: 2,
    name: '新品上市推广',
    type: 'new_product',
    startTime: '2025-10-15 00:00:00',
    endTime: '2025-10-22 23:59:59',
    status: '已结束',
    budget: '4.7万',
    participants: '430'
  },
  {
    id: 3,
    name: '品牌联合营销',
    type: 'brand_cooperation',
    startTime: '2025-09-20 00:00:00',
    endTime: '2025-09-27 23:59:59',
    status: '已结束',
    budget: '2.3万',
    participants: '120'
  }
])

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

const viewActivityDetail = (id) => ElMessage.info('查看活动详情')
const cancelActivity = (id) => {
  const activity = marketingActivities.value.find(a => a.id === id)
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
</script>

<style scoped>
.tab-content {
  padding: 20px 0;
}
.activity-create,
.activity-list-section {
  margin-bottom: 30px;
}
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