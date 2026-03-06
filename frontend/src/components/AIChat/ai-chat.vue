<template>
  <div class="mobile-chatbot-container">
    <div class="chat-main" ref="scrollContainer">
      <div v-for="(msg, index) in messages" :key="index" class="message-row">
        <t-comment
          :author="msg.role === 'user' ? '用户' : '知湘知味'"
          :datetime="msg.datetime"
        >
          <template #avatar>
            <t-avatar :hide-on-load-failed="false" :content="msg.role === 'user' ? '用户' : '知'">
            </t-avatar>
          </template>
      
          <template #content>
            <div v-if="msg.reasoning || msg.isThinking" class="think-box">
              <div class="think-head" @click="msg.showReasoning = !msg.showReasoning">
                <t-loading v-if="msg.isThinking" size="small" class="mr-2" />
                <span v-else class="mr-2"></span>
                <span class="think-title">{{ msg.isThinking ? '正在思考中...' : '已思考完成' }}</span>
                <span class="think-arrow">{{ msg.showReasoning ? '▲' : '▼' }}</span>
              </div>
              <div v-if="msg.showReasoning" class="think-content">
                {{ msg.reasoning || '正在梳理逻辑...' }}
              </div>
            </div>
            
            <vue-markdown :source="msg.content" class="answer-text" /> 
          </template>
        </t-comment>
      </div>
      <div v-if="loading && !messages.some(m => m.isThinking)" class="p-4">
        <t-loading text="正在连接服务器..." size="small" />
      </div>
    </div>

    <div class="chat-footer">
      <t-textarea
        v-model="inputBuffer"
        placeholder="输入咨询内容，Shift+Enter 换行"
        :autosize="{ minRows: 1, maxRows: 4 }"
        @keydown.enter="handleTDesignKeydown"
      />
      <t-button :loading="loading" theme="primary" shape="circle" @click="handleSend">
        <mdicon name="send" color="#fff"/>
      </t-button>
    </div>
    <div class="footer">知湘知味 是一款 AI 工具，其回答未必正确无误。</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue';
import VueMarkdown from 'vue-markdown-render';

interface Props {
  systemRole?: string;
  contextData?: any;
}
const props = withDefaults(defineProps<Props>(), {
  systemRole: "你是一个专业的智能助手。",
  contextData: () => ({})
});

const messages = ref<any[]>([]);
const inputBuffer = ref('');
const loading = ref(false);
const scrollContainer = ref<HTMLElement | null>(null);

const API_ENDPOINT = import.meta.env.VITE_OPENAI_API_ENDPOINT;
const API_KEY = import.meta.env.VITE_OPENAI_API_SERCET;

const finalSystemPrompt = computed(() => {
  let content = props.systemRole;
  if (props.contextData && Object.keys(props.contextData).length > 0) {
    content += `\n\n[上下文数据]: ${JSON.stringify(props.contextData)}`;
  }
  return content;
});

const handleTDesignKeydown = (val: string, context: { e: KeyboardEvent }) => {
  const e = context?.e;
  if (!e) return;
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
};

const handleSend = async () => {
  const text = inputBuffer.value.trim();
  if (!text || loading.value) return;

  messages.value.push({
    role: 'user',
    content: text,
    datetime: new Date().toLocaleTimeString()
  });

  const assistantMsg = {
    role: 'assistant',
    content: '',
    reasoning: '',
    isThinking: false,
    showReasoning: true,
    datetime: new Date().toLocaleTimeString()
  };
  messages.value.push(assistantMsg);
  
  const currentIdx = messages.value.length - 1;
  inputBuffer.value = '';
  loading.value = true;
  await scrollToBottom();

  try {
    const sanitizedHistory = messages.value
      .slice(0, -1)
      .filter(m => m.content && m.content.trim() !== '')
      .map(m => ({ role: m.role, content: m.content }));

    const response = await fetch(`${API_ENDPOINT}/v1/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      body: JSON.stringify({
        model: 'qwen3-8b',
        messages: [{ role: 'system', content: finalSystemPrompt.value }, ...sanitizedHistory],
        stream: true
      })
    });

    if (!response.ok) throw new Error(`Status: ${response.status}`);

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let isInsideThink = false;

    while (reader) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed.startsWith('data: ') || trimmed === 'data: [DONE]') continue;

        try {
          const json = JSON.parse(trimmed.slice(6));
          const delta = json.choices[0]?.delta?.content || '';
          const target = messages.value[currentIdx];

          if (delta.includes('<think>')) {
            isInsideThink = true;
            target.isThinking = true;
            continue;
          }
          if (delta.includes('</think>')) {
            isInsideThink = false;
            target.isThinking = false;
            setTimeout(() => { target.showReasoning = false; }, 1500);
            continue;
          }

          if (isInsideThink) {
            target.reasoning += delta;
          } else {
            target.content += delta;
          }
          scrollToBottom();
        } catch (e) {}
      }
    }
  } catch (err) {
    messages.value[currentIdx].content = "无法连接到LLM 服务器，请确认服务已启动。";
  } finally {
    loading.value = false;
    messages.value[currentIdx].isThinking = false;
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
  background-color: white;
  max-width: 100%;
}

.chat-main {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  text-align: start;
}

.think-box {
  background: var(--td-bg-color-container-hover);
  border-left: 3px solid var(--td-brand-color);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
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

.think-content {
  padding: 10px 12px;
  font-size: 13px;
  color: var(--td-text-color-placeholder);
  border-top: 1px solid var(--td-component-border);
  font-style: italic;
  white-space: pre-wrap;
}

/* 调整 Markdown 渲染容器的样式 */
.answer-text :deep(p) { margin: 0 0 8px 0; }
.answer-text :deep(ul), .answer-text :deep(ol) { padding-left: 20px; margin: 8px 0; }
.answer-text :deep(code) { background: #f3f3f3; padding: 2px 4px; border-radius: 3px; font-family: monospace; }
.answer-text :deep(pre) { background: #f3f3f3; padding: 12px; border-radius: 6px; overflow-x: auto; }

.chat-footer {
  padding: 12px;
  border-top: 1px solid var(--td-component-border);
  display: flex;
  gap: 10px;
  align-items: flex-end;
  background: var(--td-bg-color-container);
}

.footer{
  background-color: white;
  align-self: center;
  font-size: 0.85rem;
  padding-top: 5px;
  color: grey;
}

.mr-2 { margin-right: 8px; }
</style>