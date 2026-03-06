<template>
  <div class="marketing-strategy-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>营销中心</h1>
      <p class="subtitle">一站式营销策略管理与分析</p>
    </div>

    <!-- 功能标签页 -->
    <div class="tabs-container">
      <el-tabs v-model="activeTab" class="function-tabs">
        <el-tab-pane label="智能策略推荐" name="strategy">
          <StrategyContent />
        </el-tab-pane>
        <el-tab-pane label="营销活动管理" name="activity">
          <ActivityContent />
        </el-tab-pane>
        <el-tab-pane label="效果分析" name="analysis">
          <AnalysisContent />
        </el-tab-pane>
        <el-tab-pane label="智能洞察" name="insight">
          <InsightContent />
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import StrategyContent from './StrategyContent.vue'
import ActivityContent from './ActivityContent.vue'
import AnalysisContent from './AnalysisContent.vue'
import InsightContent from './InsightContent.vue'

const router = useRouter()
const activeTab = ref('strategy')

const handleLogout = () => {
  console.log('退出登录')
  router.push('/login')
}
</script>

<style scoped>
/* 复用之前的样式，这里只保留必要的部分，其余与之前相同 */
.marketing-strategy-container {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

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
  margin-top: 0;
}
</style>