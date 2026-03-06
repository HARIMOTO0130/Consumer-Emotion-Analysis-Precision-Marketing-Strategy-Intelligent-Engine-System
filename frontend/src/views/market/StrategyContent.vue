<template>
  <div class="tab-content">
    <div class="recommendation-config">
      <h3>策略推荐配置</h3>
      <el-form :model="recommendationForm" label-width="120px" class="recommendation-form">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="目标受众">
              <el-select v-model="recommendationForm.audience" placeholder="请选择目标受众" style="width: 100%">
                <el-option label="全体用户" value="全体用户" />
                <el-option label="新用户" value="新用户" />
                <el-option label="老用户" value="老用户" />
                <el-option label="高价值用户" value="高价值用户" />
                <el-option label="流失风险用户" value="流失风险用户" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="营销目标">
              <el-select v-model="recommendationForm.goal" placeholder="请选择营销目标" style="width: 100%">
                <el-option label="提升转化率" value="提升转化率" />
                <el-option label="增加客单价" value="增加客单价" />
                <el-option label="提高复购率" value="提高复购率" />
                <el-option label="提升品牌知名度" value="提升品牌知名度" />
                <el-option label="减少用户流失" value="减少用户流失" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="预算范围">
              <el-select v-model="recommendationForm.budget" placeholder="请选择预算范围" style="width: 100%">
                <el-option label="低预算（<10万）" value="低预算" />
                <el-option label="中预算（10-50万）" value="中预算" />
                <el-option label="高预算（>50万）" value="高预算" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="活动周期">
              <el-select v-model="recommendationForm.period" placeholder="请选择活动周期" style="width: 100%">
                <el-option label="短期（1-3天）" value="短期" />
                <el-option label="中期（4-7天）" value="中期" />
                <el-option label="长期（8-30天）" value="长期" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="关键因素">
              <el-checkbox-group v-model="recommendationForm.factors">
                <el-checkbox label="情感倾向" value="情感倾向" />
                <el-checkbox label="购买历史" value="购买历史" />
                <el-checkbox label="浏览行为" value="浏览行为" />
                <el-checkbox label="地域分布" value="地域分布" />
                <el-checkbox label="竞品活动" value="竞品活动" />
                <el-checkbox label="季节因素" value="季节因素" />
              </el-checkbox-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="margin-top: 20px">
          <el-col :span="8">
            <el-button type="primary" :loading="isGenerating" @click="generateRecommendations" style="width: 100%">
              生成策略推荐
            </el-button>
          </el-col>
          <el-col :span="8">
            <el-button @click="resetRecommendationForm" style="width: 100%">重置</el-button>
          </el-col>
        </el-row>
      </el-form>
    </div>

    <div class="recommendation-results">
      <h3>智能策略推荐结果</h3>
      <div class="strategy-cards">
        <div v-for="strategy in recommendedStrategies" :key="strategy.id" class="strategy-card" :class="`priority-${strategy.priorityKey}`">
          <div class="strategy-header">
            <div class="strategy-title">
              <h4>{{ strategy.name }}</h4>
            </div>
            <div class="strategy-meta">
              <span class="priority-tag" :class="`priority-${strategy.priorityKey}`">
                {{ strategy.priority }}优先级
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
            </div>
          </div>
          <div class="strategy-actions">
            <el-button type="primary" @click="adoptStrategy(strategy.name)">采纳策略</el-button>
            <el-button @click="previewStrategy(strategy)">预览详情</el-button>
          </div>
        </div>
      </div>
    </div>

    <el-dialog
      v-model="chatDialogVisible"
      title="智慧策略咨询"
      width="450px"
      class="mobile-chat-dialog"
      :destroy-on-close="true"
      center
    >
      <ai-chat 
        :system-role="chatSystemRole" 
        :context-data="currentChatContext" 
      />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import AiChat from '../../components/AIChat/ai-chat.vue'

const API_ENDPOINT = import.meta.env.VITE_OPENAI_API_ENDPOINT;
const API_KEY = import.meta.env.VITE_OPENAI_API_SERCET;

const recommendationForm = ref({
  audience: '',
  goal: '',
  budget: '',
  period: '',
  factors: []
})

const isGenerating = ref(false)
const chatDialogVisible = ref(false)
const currentChatContext = ref({})
const chatSystemRole = ref("你是一个专注与分析湘菜市场的分析师，请基于提供的策略详情回答用户的疑问。")

// 优先级颜色映射
const priorityMap = { '高': 'high', '中': 'medium', '低': 'low', 'high': 'high', 'medium': 'medium', 'low': 'low' }

// 保留原有的 Mock 数据，并增加 rawDetail 以支持预览对话
const recommendedStrategies = ref([
  {
    id: 1,
    name: '新用户注册礼包',
    description: '针对新用户推出注册礼包，提高注册转化率和首次购买率',
    audience: '新用户',
    budget: '5-10万',
    expectedEffect: 35,
    priority: '高',
    priorityKey: 'high',
    rawDetail: { action: ["发放新人券", "短信提醒"], pros: ["获客快"], cons: ["核销成本高"] }
  },
  {
    id: 2,
    name: '老用户复购优惠',
    description: '针对30天未复购的老用户推出专属优惠，提高复购率',
    audience: '老用户',
    budget: '10-15万',
    expectedEffect: 28,
    priority: '中',
    priorityKey: 'medium',
    rawDetail: { action: ["定向推送券", "会员日双倍积分"], pros: ["精准度高"], cons: ["用户疲劳"] }
  },
  {
    id: 3,
    name: '高价值用户专属活动',
    description: '为高价值用户打造专属活动，提升品牌忠诚度和客单价',
    audience: '高价值用户',
    budget: '15-20万',
    expectedEffect: 42,
    priority: '高',
    priorityKey: 'high',
    rawDetail: { action: ["线下主厨私宴", "定制礼盒"], pros: ["粘性极强"], cons: ["覆盖范围窄"] }
  },
  {
    id: 4,
    name: '流失风险用户挽回',
    description: '针对流失风险用户推出个性化挽回方案，减少用户流失',
    audience: '流失风险用户',
    budget: '8-12万',
    expectedEffect: 22,
    priority: '中',
    priorityKey: 'medium',
    rawDetail: { action: ["召回短信", "赠送回归菜品"], pros: ["止损作用明显"], cons: ["挽回率波动大"] }
  }
])

const generateRecommendations = async () => {
  if (!recommendationForm.value.audience || !recommendationForm.value.goal) {
    ElMessage.warning('请选择目标受众和营销目标')
    return
  }

  isGenerating.value = true
  const optionsString = JSON.stringify(recommendationForm.value)
  
  const prompt = `你是一个专注与分析湘菜市场的分析师，现在用户需要你给出智慧策略推荐,根据"""${optionsString}""""，你需要按照下面的json格式输出，不要包含任何推理过程，只返回JSON内容：
  {
    "title":"策略标题",
    "desc":"简短描述",
    "priority":"高|低|中",
    "priority_weight":0.85,
    "cost":"10-15万元",
    "detail":{
        "action":["首先...","然后..."],
        "pros":["优点1"],
        "cons":["风险1"]
    }
  }`

  try {
    const response = await fetch(`${API_ENDPOINT}/v1/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      body: JSON.stringify({
        model: 'qwen3-8b',
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.7
      })
    })

    const data = await response.json()
    let content = data.choices[0].message.content
    content = content.replace(/<think>[\s\S]*?<\/think>/gi, '').replace(/```json|```/g, '').trim()
    
    const result = JSON.parse(content)
    
    const newStrategy = {
      id: Date.now(),
      name: result.title || "AI 智能策略",
      description: result.desc || "暂无描述",
      audience: recommendationForm.value.audience,
      budget: result.cost || "根据配置估算",
      expectedEffect: Math.floor((result.priority_weight || 0.5) * 100),
      priority: result.priority || '中',
      priorityKey: priorityMap[result.priority] || 'medium',
      rawDetail: result.detail 
    }

    recommendedStrategies.value.unshift(newStrategy)
    ElMessage.success('AI 策略推荐生成成功！')
  } catch (err) {
    console.error("LLM Error:", err)
    ElMessage.error('生成异常，已添加模拟策略。')
    addMockStrategy()
  } finally {
    isGenerating.value = false
  }
}

// 异常兜底逻辑
const addMockStrategy = () => {
  recommendedStrategies.value.unshift({
    id: Date.now(),
    name: '湘菜口味季节性调整 (自动生成)',
    description: '根据季节变换动态调整辣度比例',
    audience: recommendationForm.value.audience || '全体用户',
    budget: '5万',
    expectedEffect: 18,
    priority: '中',
    priorityKey: 'medium',
    rawDetail: { action: ["调整菜单"], pros: ["口感适配"], cons: ["物料更新"] }
  })
}

const resetRecommendationForm = () => {
  recommendationForm.value = { audience: '', goal: '', budget: '', period: '', factors: [] }
}

const adoptStrategy = (name) => ElMessage.success(`策略【${name}】已采纳！`)

const previewStrategy = (strategy) => {
  // 注入上下文数据，供 AiChat 组件使用
  currentChatContext.value = {
    策略名称: strategy.name,
    受众: strategy.audience,
    预算: strategy.budget,
    核心路径: strategy.rawDetail?.action || [],
    优势分析: strategy.rawDetail?.pros || [],
    风险预警: strategy.rawDetail?.cons || []
  }
  chatDialogVisible.value = true
}
</script>

<style scoped>
.tab-content { padding: 20px 0; }
.recommendation-config, .recommendation-results { margin-bottom: 30px; }
.recommendation-config h3, .recommendation-results h3 {
  font-size: 18px; margin-bottom: 20px; color: #333;
  border-bottom: 2px solid #409eff; padding-bottom: 10px;
}
.recommendation-form { background-color: #f9f9f9; padding: 20px; border-radius: 8px; }

.strategy-cards {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 20px;
}
.strategy-card {
  background-color: #fff; border-radius: 8px; padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); transition: all 0.3s;
}
.strategy-card:hover { transform: translateY(-5px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); }
.strategy-card.priority-high { border-left: 4px solid #f56c6c; }
.strategy-card.priority-medium { border-left: 4px solid #e6a23c; }
.strategy-card.priority-low { border-left: 4px solid #67c23a; }

.strategy-header { display: flex; justify-content: space-between; margin-bottom: 15px; }
.priority-tag { padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.priority-tag.priority-high { background: #fef0f0; color: #f56c6c; }
.priority-tag.priority-medium { background: #fdf6ec; color: #e6a23c; }
.priority-tag.priority-low { background: #f0f9eb; color: #67c23a; }

.expected-effect { font-weight: bold; color: #409eff; margin-top: 4px; }
.strategy-description { color: #666; font-size: 14px; margin-bottom: 15px; min-height: 42px; line-height: 1.5; }
.strategy-details { display: flex; gap: 20px; margin-bottom: 20px; }
.detail-label { font-size: 12px; color: #999; display: block; }
.detail-value { font-weight: bold; font-size: 14px; color: #333; }

.strategy-actions { display: flex; gap: 10px; }

/* Dialog 移动端风格优化 */
:deep(.el-dialog) {
  border-radius: 12px;
}
:deep(.el-dialog__body) {
  padding: 0; 
  background-color: #f5f5f5;
}

@media (max-width: 768px) {
  .strategy-cards { grid-template-columns: 1fr; }
}
</style>