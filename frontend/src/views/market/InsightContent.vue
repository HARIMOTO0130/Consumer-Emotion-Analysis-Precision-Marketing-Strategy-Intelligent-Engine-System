<template>
  <div class="tab-content">
    <!-- 智能洞察列表 -->
    <div class="insights-section">
      <h3>智能营销洞察</h3>
      <div class="insights-list">
        <div v-for="insight in marketingInsights" :key="insight.id" class="insight-card" :class="`type-${insight.type}`">
          <div class="insight-header">
            <div class="insight-type">
              <span class="type-label">{{ getInsightTypeLabel(insight.type) }}</span>
            </div>
            <div class="insight-meta">
              <span class="insight-date">{{ insight.date }}</span>
              <span class="insight-priority" :class="`priority-${insight.priority}`">{{ insight.priority }}</span>
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
            <el-button type="primary" size="small" @click="takeInsightAction(insight.id)">执行行动</el-button>
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
              <div class="trend-item"><span class="trend-date">今天</span><span class="trend-value positive">72.5%</span></div>
              <div class="trend-item"><span class="trend-date">1天后</span><span class="trend-value positive">73.2%</span></div>
              <div class="trend-item"><span class="trend-date">3天后</span><span class="trend-value positive">74.8%</span></div>
              <div class="trend-item"><span class="trend-date">7天后</span><span class="trend-value positive">76.5%</span></div>
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
              <div class="type-item"><span class="type-name">促销活动</span><span class="type-effect positive">+25%</span></div>
              <div class="type-item"><span class="type-name">新品发布</span><span class="type-effect positive">+35%</span></div>
              <div class="type-item"><span class="type-name">品牌合作</span><span class="type-effect positive">+20%</span></div>
              <div class="type-item"><span class="type-name">内容营销</span><span class="type-effect positive">+15%</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

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
  // ... 其余数据
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

const getInsightTypeLabel = (type) => {
  const labels = { opportunity: '机会发现', risk: '风险预警', trend: '趋势洞察', insight: '智能洞察' }
  return labels[type] || '智能洞察'
}

const takeInsightAction = (id) => ElMessage.success('已执行洞察建议！')
</script>

<style scoped>
.tab-content {
  padding: 20px 0;
}
.insights-section,
.trend-prediction {
  margin-bottom: 30px;
}
.insights-section h3,
.trend-prediction h3 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 2px solid var(--color-primary-hover);
  padding-bottom: 10px;
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
  border-left: 4px solid var(--color-danger);
}
.insight-card.type-trend {
  border-left: 4px solid var(--color-primary-hover);
}
.insight-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}
.insight-type .type-label {
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
@media (max-width: 768px) {
  .insights-list,
  .prediction-cards {
    grid-template-columns: 1fr;
  }
}
</style>