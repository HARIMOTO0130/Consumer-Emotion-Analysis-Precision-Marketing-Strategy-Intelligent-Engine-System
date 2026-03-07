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
      :title="`策略咨询: ${currentChatContext.策略名称 || ''}`"
      width="1000px"
      class="strategy-dialog"
      :destroy-on-close="true"
    >
      <div class="strategy-preview-container">
        <div class="details-side">
          <div class="side-scroll-content">
            <div class="detail-section">
              <h4 class="section-title">执行路径</h4>
              <el-timeline>
                <el-timeline-item
                  v-for="(step, index) in currentChatContext.核心路径"
                  :key="index"
                  :timestamp="`阶段 ${index + 1}`"
                  placement="top"
                  type="primary"
                >
                  {{ step }}
                </el-timeline-item>
              </el-timeline>
            </div>

            <div class="detail-section">
              <h4 class="section-title">优劣势评估</h4>
              <div class="analysis-box">
                <div v-for="pro in currentChatContext.优势分析" :key="pro" class="eval-card pro-card">
                  <span class="dot">●</span> {{ pro }}
                </div>
                <div v-for="con in currentChatContext.风险预警" :key="con" class="eval-card con-card">
                  <span class="dot">●</span> {{ con }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="chat-side">
          <ai-chat 
            :system-role="chatSystemRole" 
            :context-data="currentChatContext" 
          />
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import AiChat from '../../components/AIChat/ai-chat.vue'

const API_ENDPOINT = import.meta.env.VITE_OPENAI_API_ENDPOINT;
const API_KEY = import.meta.env.VITE_OPENAI_API_SERCET;

const recommendationForm = ref({ audience: '', goal: '', budget: '', period: '', factors: [] })
const isGenerating = ref(false)
const chatDialogVisible = ref(false)
const currentChatContext = ref({})
const chatSystemRole = ref("你是一个专注湘菜市场的资深营销顾问。请结合左侧展示的策略步骤、优势和风险，为用户提供落地建议。")

const priorityMap = { '高': 'high', '中': 'medium', '低': 'low', 'high': 'high', 'medium': 'medium', 'low': 'low' }

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
    rawDetail: { action: ["发放新人优惠券", "短信提醒核销", "三天后二次触达"], pros: ["拉新效果显著"], cons: ["核销成本高"] }
  }
])

const generateRecommendations = async () => {
  if (!recommendationForm.value.audience || !recommendationForm.value.goal) {
    ElMessage.warning('请选择目标受众和营销目标')
    return
  }

  isGenerating.value = true
  const optionsString = JSON.stringify(recommendationForm.value)
  
  // 优化后的 Prompt (包含 One-shot)
  const prompt = `你是一个资深湘菜市场分析师。请根据配置给出深度策略。
  ### 要求：
  1. 标题先行，内容必须结构化且具有强落地性。
  2. detail.action 必须是按先后顺序执行的步骤。
  3. 严禁任何解释文字，只返回 JSON。

  ### One-shot 示例：
  Input: {"audience":"新用户","goal":"提升转化率"}
  Output: {
    "title":"“入湘随俗”首单破冰计划",
    "desc":"针对新用户通过爆款单品5折券引导进店消费，建立品牌味觉记忆。",
    "priority":"高",
    "priority_weight":0.9,
    "cost":"2-5万",
    "detail":{
      "action":["基于LBS投放朋友圈广告","引导领取5折招牌菜券","门店扫码转化会员"],
      "pros":["引流精准","转化路径短"],
      "cons":["毛利短期受损"]
    }
  }

  ### 待处理输入：
  ${optionsString}`

  try {
    const response = await fetch(`${API_ENDPOINT}/v1/chat/completions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${API_KEY}` },
      body: JSON.stringify({
        model: 'qwen3-8b',
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.3 // 降低随机性，保证结构化稳定
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
    ElMessage.error('生成异常，已添加模拟策略。')
    addMockStrategy()
  } finally {
    isGenerating.value = false
  }
}

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
    rawDetail: { action: ["调研当季口味", "更新菜单物料"], pros: ["口感适配"], cons: ["物料更新快"] }
  })
}

const resetRecommendationForm = () => { recommendationForm.value = { audience: '', goal: '', budget: '', period: '', factors: [] } }
const adoptStrategy = (name) => ElMessage.success(`策略【${name}】已采纳！`)

const previewStrategy = (strategy) => {
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

.strategy-cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 20px; }
.strategy-card { background-color: #fff; border-radius: 8px; padding: 20px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); transition: all 0.3s; border-left: 4px solid #ddd; }
.strategy-card:hover { transform: translateY(-5px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); }
.strategy-card.priority-high { border-left-color: #f56c6c; }
.strategy-card.priority-medium { border-left-color: #e6a23c; }
.strategy-card.priority-low { border-left-color: #67c23a; }

.strategy-header { display: flex; justify-content: space-between; margin-bottom: 15px; }
.priority-tag { padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.priority-tag.priority-high { background: #fef0f0; color: #f56c6c; }
.priority-tag.priority-medium { background: #fdf6ec; color: #e6a23c; }
.priority-tag.priority-low { background: #f0f9eb; color: #67c23a; }

.expected-effect { font-weight: bold; color: #409eff; }
.strategy-description { text-align: start; color: #666; font-size: 14px; margin-bottom: 15px; min-height: 42px; }
.strategy-details { display: flex; gap: 20px; margin-bottom: 20px; }
.detail-label { font-size: 12px; color: #999; display: block; }
.detail-value { font-weight: bold; font-size: 14px; color: #333; }
.strategy-actions { display: flex; gap: 10px; }

/* 预览弹窗双栏布局 */
.strategy-preview-container {
  display: flex;
  height: 600px; /* 固定高度确保滚动 */
  background-color: #fff;
}

.details-side {
  flex: 0 0 400px;
  border-right: 1px solid #ebeef5;
  background-color: #fff;
}

.side-scroll-content {
  padding: 20px;
  height: 100%;
  overflow-y: auto;
}

.chat-side {
  flex: 1;
  background-color: #fff;
  display: flex;
  flex-direction: column;
}

.detail-section { margin-bottom: 25px; }
.section-title { font-size: 15px; color: #333; margin-bottom: 15px; padding-left: 10px; border-left: 3px solid #409eff; }

.analysis-box { display: flex; flex-direction: column; gap: 10px; }
.eval-card { padding: 10px 15px; border-radius: 6px; font-size: 13px; border: 1px solid transparent; }
.pro-card { background-color: #fff; color: #67c23a; border-color: #e1f3d8; }
.con-card { background-color: #fff; color: #f56c6c; border-color: #fde2e2; }
.eval-card .dot { margin-right: 5px; font-size: 10px; vertical-align: middle; }

/* 隐藏左侧滚动条美化 */
.side-scroll-content::-webkit-scrollbar { width: 5px; }
.side-scroll-content::-webkit-scrollbar-thumb { background: #ccc; border-radius: 10px; }

:deep(.el-dialog__body) { padding: 0 !important; }
:deep(.el-timeline-item__content) { font-size: 13px; color: #444; }

@media (max-width: 900px) {
  .strategy-preview-container { flex-direction: column; height: auto; }
  .details-side { flex: none; width: 100%; max-height: 300px; }
}
</style>