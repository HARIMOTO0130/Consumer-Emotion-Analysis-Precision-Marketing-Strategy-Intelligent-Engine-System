<template>
  <div class="tab-content">
    <!-- 策略推荐配置 -->
    <div class="recommendation-config">
      <h3>策略推荐配置</h3>
      <el-form :model="recommendationForm" label-width="120px" class="recommendation-form">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="目标受众">
              <el-select v-model="recommendationForm.audience" placeholder="请选择目标受众" style="width: 100%">
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
              <el-select v-model="recommendationForm.goal" placeholder="请选择营销目标" style="width: 100%">
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
              <el-select v-model="recommendationForm.budget" placeholder="请选择预算范围" style="width: 100%">
                <el-option label="低预算（<10万）" value="low" />
                <el-option label="中预算（10-50万）" value="medium" />
                <el-option label="高预算（>50万）" value="high" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="活动周期">
              <el-select v-model="recommendationForm.period" placeholder="请选择活动周期" style="width: 100%">
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
            <el-button type="primary" @click="generateRecommendations" style="width: 100%">生成策略推荐</el-button>
          </el-col>
          <el-col :span="8">
            <el-button @click="resetRecommendationForm" style="width: 100%">重置</el-button>
          </el-col>
        </el-row>
      </el-form>
    </div>

    <!-- 策略推荐结果 -->
    <div class="recommendation-results">
      <h3>智能策略推荐结果</h3>
      <div class="strategy-cards">
        <div v-for="strategy in recommendedStrategies" :key="strategy.id" class="strategy-card" :class="`priority-${strategy.priority}`">
          <div class="strategy-header">
            <div class="strategy-title">
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
            <el-button type="primary" @click="adoptStrategy(strategy.id)">采纳策略</el-button>
            <el-button @click="previewStrategy(strategy.id)">预览详情</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const recommendationForm = ref({
  audience: '',
  goal: '',
  budget: '',
  period: '',
  factors: []
})

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
  // ... 其余数据同上
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

const adoptStrategy = (id) => ElMessage.success('策略已采纳！')
const previewStrategy = (id) => ElMessage.info('预览策略详情')
</script>

<style scoped>
/* 从原文件中复制 .tab-content 内的样式即可 */
.tab-content {
  padding: 20px 0;
}
.recommendation-config,
.recommendation-results {
  margin-bottom: 30px;
}
.recommendation-config h3,
.recommendation-results h3 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 2px solid var(--color-primary-hover);
  padding-bottom: 10px;
}
.recommendation-form {
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
  border-left: 4px solid var(--color-danger);
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
@media (max-width: 768px) {
  .strategy-cards {
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