<template>
  <div class="login-container">
    <div class="login-wrapper">
      <!-- 登录头部 -->
      <div class="login-header">
        <h1 class="system-title">🎯 消费者情感分析与精准营销策略的智能引擎</h1>
        <p class="system-subtitle">Consumer Emotion Analysis & Precision Marketing Strategy Intelligent Engine System</p>
      </div>
      
      <!-- 登录表单 -->
      <div class="login-form-container">
        <div class="login-form-header">
          <h2>🔐 系统登录</h2>
          <p>请输入您的账号和密码登录系统</p>
        </div>
        
        <el-form 
          :model="loginForm" 
          :rules="loginRules" 
          ref="loginFormRef" 
          class="login-form"
          label-position="top"
        >
          <el-form-item prop="username" class="form-item-with-feedback">
            <el-input 
              v-model="loginForm.username" 
              placeholder="请输入账号" 
              prefix-icon="User"
              clearable
              @focus="onInputFocus('username')"
              @blur="onInputBlur('username')"
              :class="{ 'input-focused': focusedInput === 'username' }"
            />
          </el-form-item>
          
          <el-form-item prop="password" class="form-item-with-feedback">
            <el-input 
              v-model="loginForm.password" 
              type="password" 
              placeholder="请输入密码" 
              prefix-icon="Lock"
              show-password
              @focus="onInputFocus('password')"
              @blur="onInputBlur('password')"
              :class="{ 'input-focused': focusedInput === 'password' }"
            />
          </el-form-item>
          
          <el-form-item class="form-item-with-feedback">
            <div class="form-item-row">
              <el-checkbox 
                v-model="loginForm.remember"
                @change="onRememberChange"
                class="remember-checkbox"
              >
                记住我
              </el-checkbox>
              <el-link 
                type="primary" 
                class="forgot-password"
                @click="handleForgotPassword"
                :underline="false"
              >
                忘记密码？
              </el-link>
            </div>
          </el-form-item>
          
          <el-form-item class="form-item-with-feedback">
            <el-button 
              type="primary" 
              class="login-button" 
              @click="handleLogin"
              :loading="loading"
              :icon="loading ? '' : 'Check'"
              round
            >
              {{ loading ? '登录中...' : '登录' }}
            </el-button>
          </el-form-item>
        </el-form>
        
        <!-- 登录状态提示 -->
        <div v-if="loginStatus" class="login-status" :class="loginStatus.type">
          {{ loginStatus.message }}
        </div>
      </div>
      
      <!-- 登录底部 -->
      <div class="login-footer">
        <p>© 2023 消费者情感分析与精准营销策略的智能引擎系统. 保留所有权利.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)
const loginStatus = ref(null)
const focusedInput = ref('')

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: '',
  remember: false
})

// 输入框聚焦处理
const onInputFocus = (field) => {
  focusedInput.value = field
}

// 输入框失焦处理
const onInputBlur = (field) => {
  focusedInput.value = ''
}

// 记住我选项变更处理
const onRememberChange = (value) => {
  console.log('记住我选项变更为:', value)
  // 这里可以添加本地存储逻辑
}

// 忘记密码处理
const handleForgotPassword = () => {
  ElMessage({
    message: '忘记密码功能正在开发中，请联系管理员',
    type: 'info',
    duration: 3000
  })
}

// 登录表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入账号', trigger: 'blur' },
    { min: 3, max: 20, message: '账号长度应在3-20个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  // 表单验证
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    
    // 显示加载状态
    loading.value = true
    
    // 模拟登录请求
    setTimeout(() => {
      // 简单的登录验证（实际项目中应该调用后端API）
      if (loginForm.username === 'admin' && loginForm.password === 'admin123') {
        // 登录成功
        loginStatus.value = {
          type: 'success',
          message: '登录成功！正在跳转...'
        }
        
        // 模拟跳转延迟
        setTimeout(() => {
          router.push('/')
        }, 1000)
      } else {
        // 登录失败
        loginStatus.value = {
          type: 'error',
          message: '账号或密码错误，请重新输入'
        }
        
        // 3秒后清除错误提示
        setTimeout(() => {
          loginStatus.value = null
        }, 3000)
      }
      
      // 隐藏加载状态
      loading.value = false
    }, 1500)
  } catch (error) {
    console.error('表单验证失败:', error)
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-wrapper {
  width: 100%;
  max-width: 800px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.login-header {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.system-title {
  font-size: 24px;
  margin-bottom: 10px;
  color: #333;
  font-weight: bold;
}

.system-subtitle {
  font-size: 14px;
  color: #666;
}

.login-form-container {
  padding: 40px;
}

.login-form-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-form-header h2 {
  font-size: 24px;
  margin-bottom: 10px;
  color: #333;
}

.login-form-header p {
  font-size: 14px;
  color: #666;
}

.login-form {
  max-width: 400px;
  margin: 0 auto;
}

.form-item-with-feedback {
  margin-bottom: 24px;
  transition: all 0.3s ease;
}

.form-item-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.remember-checkbox {
  font-size: 14px;
  color: #546e7a;
  cursor: pointer;
  transition: all 0.3s ease;
}

.remember-checkbox:hover {
  color: #1890ff;
  transform: translateY(-1px);
}

.forgot-password {
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
}

.forgot-password:hover {
  color: #40a9ff;
  text-decoration: underline;
  transform: translateY(-1px);
}

.login-button {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.3);
}

.login-button:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 4px 16px rgba(24, 144, 255, 0.4);
}

.login-button:disabled {
  transform: none;
  box-shadow: none;
}

.login-status {
  margin-top: 24px;
  padding: 16px;
  border-radius: 8px;
  text-align: center;
  font-size: 14px;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.login-status.success {
  background-color: rgba(82, 196, 26, 0.1);
  color: #52c41a;
  border-color: rgba(82, 196, 26, 0.3);
  box-shadow: 0 2px 8px rgba(82, 196, 26, 0.2);
}

.login-status.error {
  background-color: rgba(255, 77, 79, 0.1);
  color: #ff4d4f;
  border-color: rgba(255, 77, 79, 0.3);
  box-shadow: 0 2px 8px rgba(255, 77, 79, 0.2);
}

/* 输入框交互样式 */
.input-focused {
  border-color: #1890ff !important;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2) !important;
  transition: all 0.3s ease !important;
}

/* 表单验证反馈样式 */
.el-form-item.is-error .el-input__wrapper {
  box-shadow: 0 0 0 2px rgba(255, 77, 79, 0.2) !important;
}

.el-form-item.is-success .el-input__wrapper {
  box-shadow: 0 0 0 2px rgba(82, 196, 26, 0.2) !important;
}

/* 按钮加载动画优化 */
.el-button--loading .el-icon-loading {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.login-footer {
  text-align: center;
  padding: 20px;
  background-color: #f5f5f5;
  border-top: 1px solid #e8e8e8;
}

.login-footer p {
  font-size: 12px;
  color: #999;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-wrapper {
    max-width: 100%;
    margin: 20px;
  }
  
  .login-form-container {
    padding: 20px;
  }
  
  .system-title {
    font-size: 20px;
  }
  
  .login-form-header h2 {
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .login-header {
    padding: 30px 15px;
  }
  
  .system-title {
    font-size: 18px;
  }
  
  .system-subtitle {
    font-size: 12px;
  }
  
  .login-form-header {
    margin-bottom: 20px;
  }
  
  .login-form-header h2 {
    font-size: 18px;
  }
  
  .login-button {
    padding: 10px;
    font-size: 14px;
  }
}
</style>