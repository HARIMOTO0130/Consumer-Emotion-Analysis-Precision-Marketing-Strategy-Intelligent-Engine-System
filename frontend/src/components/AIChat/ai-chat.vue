<template>
  <div class="mobile-chatbot-container">
    <div class="chat-main" ref="scrollContainer">
      <div v-for="(msg, index) in messages" :key="index" class="message-row">
        <t-comment
          :author="msg.role === 'user' ? '用户' : '知湘知味助理'"
          :datetime="msg.datetime"
        >
          <template #avatar>
            <t-avatar 
              :hide-on-load-failed="false" 
              :content="msg.role === 'user' ? 'U' : '知'"
              :shape="msg.role === 'user' ? 'circle' : 'round'"
            />
          </template>
          
          <template #content>
            <div v-if="msg.reasoning || msg.isThinking" class="think-box">
              <div class="think-head" @click="msg.showReasoning = !msg.showReasoning">
                <t-loading v-if="msg.isThinking" size="small" class="mr-2" />
                <span class="think-title">
                  {{ msg.isThinking ? '正在深度思考中...' : '深度思考完成' }}
                </span>
                <span class="think-arrow">{{ msg.showReasoning ? '▲' : '▼' }}</span>
              </div>
              <div v-if="msg.showReasoning" class="think-content">
                {{ msg.reasoning || '正在检索营销知识库...' }}
              </div>
            </div>
            
            <vue-markdown :source="msg.content" class="answer-text" /> 
          </template>
        </t-comment>
      </div>

      <div v-if="loading && !messages.some(m => m.isThinking)" class="p-4">
        <t-loading text="正在连接知湘知味 AI..." size="small" />
      </div>
    </div>

    <div class="chat-footer">
      <t-textarea
        v-model="inputBuffer"
        placeholder="输入咨询内容，Enter 发送"
        :autosize="{ minRows: 1, maxRows: 4 }"
        :disabled="loading"
        @keydown="handleKeydown"
      />
      <t-button 
        :loading="loading" 
        theme="primary" 
        shape="circle" 
        @click="handleSend"
        :disabled="!inputBuffer.trim()"
      >
        <template #icon>
          <t-icon name="send" />
        </template>
      </t-button>
    </div>
    <div class="footer-note">知湘知味 是一款 AI 工具，回答仅供参考。</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed,reactive, nextTick } from 'vue';
import VueMarkdown from 'vue-markdown-render';

interface Props {
  systemRole?: string;
  contextData?: any;
}

const props = withDefaults(defineProps<Props>(), {
  systemRole: "你是一个专业的湘菜营销顾问。",
  contextData: () => ({})
});

const messages = ref<any[]>([]);
const inputBuffer = ref('');
const loading = ref(false);
const scrollContainer = ref<HTMLElement | null>(null);

const API_ENDPOINT = import.meta.env.VITE_OPENAI_API_ENDPOINT;
const API_KEY = import.meta.env.VITE_OPENAI_API_SERCET;
const API_MODEL_NAME = import.meta.env.VITE_OPENAI_API_MODEL;

const finalSystemPrompt = computed(() => {
  let content = props.systemRole;
  if (props.contextData && Object.keys(props.contextData).length > 0) {
    content += `\n\n[当前策略上下文]: ${JSON.stringify(props.contextData)}`;
  }
  return content;
});

const handleKeydown = (val: string, context: { e: KeyboardEvent }) => {
  const e = context?.e;
  if (e?.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
};

const handleSend = async () => {
  const text = inputBuffer.value.trim();
  if (!text || loading.value) return;

  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: text,
    datetime: new Date().toLocaleTimeString()
  });

  // 预设 AI 消息对象
  const assistantMsg = reactive({
    role: 'assistant',
    content: '',
    reasoning: '',
    isThinking: false,
    showReasoning: true,
    datetime: new Date().toLocaleTimeString()
  });
  messages.value.push(assistantMsg);
  
  inputBuffer.value = '';
  loading.value = true;
  await scrollToBottom();

  try {
    const history = messages.value
      .slice(0, -1)
      .map(m => ({ role: m.role, content: m.content || m.responseText }));

    const response = await fetch(`${API_ENDPOINT}/v1/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      body: JSON.stringify({
        model: API_MODEL_NAME,
        messages: [{ role: 'system', content: finalSystemPrompt.value }, ...history],
        stream: true
      })
    });

    if (!response.ok) throw new Error("Network Response Error");

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let isInsideThink = false;

    while (reader) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (!line.startsWith('data: ') || line === 'data: [DONE]') continue;

        try {
          const json = JSON.parse(line.slice(6));
          const delta = json.choices[0]?.delta?.content || '';

          // 核心逻辑：拦截 think 标签
          if (delta.includes('<think>')) {
            isInsideThink = true;
            assistantMsg.isThinking = true;
            continue;
          }
          if (delta.includes('</think>')) {
            isInsideThink = false;
            assistantMsg.isThinking = false;
            // 思考结束后延迟收起
            setTimeout(() => { assistantMsg.showReasoning = false; }, 1500);
            continue;
          }

          if (isInsideThink) {
            assistantMsg.reasoning += delta;
          } else {
            assistantMsg.content += delta;
          }
          scrollToBottom();
        } catch (e) {}
      }
    }
  } catch (err) {
    assistantMsg.content = "连接 AI 营销智库失败，请检查网络后重试。";
  } finally {
    loading.value = false;
    assistantMsg.isThinking = false;
  }
};

const scrollToBottom = async () => {
  await nextTick();
  if (scrollContainer.value) {
    scrollContainer.value.scrollTop = scrollContainer.value.scrollHeight;
  }
};
</script>

<style scoped>
.mobile-chatbot-container {
  display: flex;
  flex-direction: column;
  height: 600px; 
  background-color: var(--td-bg-color-page);
  max-width: 100%;
}

.chat-main {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  text-align: start;
  background-color: white;
}

/* 思考块样式优化 */
.think-box {
  background: var(--td-bg-color-container-hover);
  border-left: 3px solid var(--color-primary);
  border-radius: 4px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.think-head {
  padding: 8px 12px;
  font-size: 12px;
  color: var(--td-text-color-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
}

.think-title { flex: 1; font-weight: 500; }
.think-arrow { font-size: 10px; margin-left: 8px; opacity: 0.6; }

.think-content {
  padding: 10px 12px;
  font-size: 13px;
  color: #666;
  border-top: 1px solid var(--td-component-border);
  font-style: italic;
  white-space: pre-wrap;
  line-height: 1.5;
}

.answer-text {
  font-size: 14px;
  line-height: 1.6;
  color: var(--td-text-color-primary);
}
.answer-text :deep(p) { margin: 0 0 12px 0; }
.answer-text :deep(p:last-child) { margin-bottom: 0; }
.answer-text :deep(code) { 
  background: var(--td-bg-color-component); 
  padding: 2px 4px; 
  border-radius: 3px; 
  font-family: monospace; 
  color: var(--td-brand-color);
}

.chat-footer {
  padding: 16px;
  border-top: 1px solid var(--td-component-border);
  display: flex;
  gap: 12px;
  align-items: flex-end;
  background: var(--td-bg-color-container);
}

.footer-note {
  background-color: var(--td-bg-color-container);
  text-align: center;
  font-size: 12px;
  padding: 8px 0;
  color: var(--td-text-color-placeholder);
}

.mr-2 { margin-right: 8px; }
</style>