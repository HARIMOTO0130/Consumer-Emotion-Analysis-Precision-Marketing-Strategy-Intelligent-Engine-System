<template>
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
          <el-table-column prop="rank" label="排名"   />
          <el-table-column prop="name" label="话题名称"   />
          <el-table-column prop="mentionCount" label="提及次数"   />
          <el-table-column prop="sentiment" label="情感倾向"  >
            <template #default="{ row }">
              <el-tag :type="row.sentiment === '正面' ? 'success' : row.sentiment === '负面' ? 'danger' : 'info'">
                {{ row.sentiment }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="trend" label="趋势"  >
            <template #default="{ row }">
              <span :style="{ color: row.trend === '上升' ? 'green' : row.trend === '下降' ? 'red' : 'orange' }">
                {{ row.trend === '上升' ? '上升' : row.trend === '下降' ? '下降' : '平稳' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="duration" label="持续时间"   />
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { ElTable, ElTableColumn, ElTag } from 'element-plus'
import mdicon from 'vue-material-design-icons'

const props = defineProps({
  dashboardStats: {
    type: Object,
    required: true
  },
  topicClusters: {
    type: Array,
    required: true
  }
})

const emit = defineEmits([])
</script>

<style scoped>
.dashboard-section h3,
.topic-clusters h3 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 2px solid var(--color-primary-hover);
  padding-bottom: 10px;
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

.topic-clusters {
  margin-top: 30px;
}
</style>