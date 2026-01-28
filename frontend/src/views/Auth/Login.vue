<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card animate__animated animate__fadeIn">
        <div class="auth-layout">
          <div class="auth-left">
            <div class="auth-image-wrapper">
              <div class="image-overlay"></div>
              <div class="image-content">
                <h2 class="image-title">消费者情感分析与精准营销策略的智能引擎</h2>
                <p class="image-subtitle">Consumer Emotion Analysis & Precision Marketing Strategy Intelligent Engine System</p>
            </div>
            </div>
          </div>

          <div class="auth-right">
            <div class="mobile-header">
              <h1 class="mobile-title">消费者情感分析与精准营销策略的智能引擎</h1>
              <p class="mobile-subtitle">Consumer Emotion Analysis & Precision Marketing Strategy Intelligent Engine System</p>
            </div>

            <div class="form-wrapper">
              <div class="form-header">
                <h2>{{ isLogin ? '系统登录' : '用户注册' }}</h2>
                <p>{{ isLogin ? '请输入您的账号和密码登录系统' : '请输入您的账号和密码完成注册' }}</p>
              </div>
              
              <el-form 
                :model="formData" 
                :rules="formRules" 
                ref="formRef" 
                class="auth-form"
                label-position="top"
              >
                <el-form-item prop="username" class="form-item">
                  <el-input 
                    v-model="formData.username" 
                    placeholder="请输入账号" 
                    prefix-icon="User"
                    clearable
                    size="large"
                  />
                </el-form-item>
                
                <el-form-item prop="password" class="form-item">
                  <el-input 
                    v-model="formData.password" 
                    type="password" 
                    placeholder="请输入密码" 
                    prefix-icon="Lock"
                    show-password
                    size="large"
                  />
                </el-form-item>
                
                <el-form-item v-if="!isLogin" prop="confirmPassword" class="form-item">
                  <el-input 
                    v-model="formData.confirmPassword" 
                    type="password" 
                    placeholder="请确认密码" 
                    prefix-icon="Lock"
                    show-password
                    size="large"
                  />
                </el-form-item>
                
                <el-form-item v-if="isLogin" class="form-item">
                  <div class="form-options">
                    <el-checkbox 
                      v-model="formData.remember"
                      @change="onRememberChange"
                      class="remember-checkbox"
                    >
                      记住我
                    </el-checkbox>
                    <el-link 
                      type="primary" 
                      class="forgot-password"
                      @click="handleForgotPassword"
                      underline="never"
                    >
                      忘记密码？
                    </el-link>
                  </div>
                </el-form-item>
                
                <el-form-item class="form-item">
                  <el-button 
                    type="primary" 
                    class="submit-button" 
                    @click="handleSubmit"
                    :loading="loading"
                    size="large"
                    round
                  >
                    {{ loading ? (isLogin ? '登录中...' : '注册中...') : (isLogin ? '登录' : '注册') }}
                  </el-button>
                </el-form-item>
                
                <el-form-item class="form-switch">
                  <el-link 
                    type="primary" 
                    @click="toggleFormType"
                    underline="never"
                    class="switch-link"
                  >
                    {{ isLogin ? '还没有账号？立即注册' : '已有账号？立即登录' }}
                  </el-link>
                </el-form-item>
              </el-form>
              
              <div class="form-footer">
                <p>知"湘"知味团队 保留所有权利</p>
                <p>© 2025-{{ currentYear }} Consumer Emotion Analysis System</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login, register } from '@services/auth'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const isLogin = ref(true)
const currentYear = new Date().getFullYear()

const formData = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  remember: false
})

const formRules = computed(() => {
  const baseRules = {
    username: [
      { required: true, message: '请输入账号', trigger: 'blur' },
      { min: 3, max: 20, message: '账号长度应在3-20个字符之间', trigger: 'blur' }
    ],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' }
    ]
  }
  
  if (!isLogin.value) {
    baseRules.confirmPassword = [
      { required: true, message: '请确认密码', trigger: 'blur' },
      { 
        validator: (rule, value, callback) => {
          if (value !== formData.password) {
            callback(new Error('两次输入的密码不一致'))
          } else {
            callback()
          }
        }, 
        trigger: 'blur' 
      }
    ]
  }
  
  return baseRules
})

const onRememberChange = (value) => {
  console.log('记住我选项变更为:', value)
}

const handleForgotPassword = () => {
  ElMessage({
    message: '忘记密码功能正在开发中，请联系管理员',
    type: 'info',
    duration: 3000
  })
}

const toggleFormType = () => {
  isLogin.value = !isLogin.value
  formData.username = ''
  formData.password = ''
  formData.confirmPassword = ''
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return ;
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    let result
    if (isLogin.value) {
      result = await login(formData.username, formData.password)
    } else {
      result = await register(formData.username, formData.password)
    }
    
    if (result.status) {
      ElMessage.success(isLogin.value ? "登录成功，欢迎回来！" : "注册成功，欢迎加入！")
      router.push('/')
    } else {
      ElMessage.error(result.msg || (isLogin.value ? '登录失败' : '注册失败'))
    }
    
    loading.value = false
  } catch (error) {
    console.error('表单验证失败:', error)
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background-color: #ffffff;
  box-sizing: border-box;
}

.auth-container {
  width: 100%;
  max-width: 1000px;
  margin: auto;

}

.auth-card {
  width: 100%;
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.auth-layout {
  display: flex;
  min-height: 600px;
}

/* 左侧图片区域 */
.auth-left {
  flex: 1;
  background-image: url('/img/auth_bg.webp');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  display: flex;
  align-items: end;
  justify-content: center;
  padding: 40px;
}

.auth-image-wrapper {
  position: relative;
  z-index: 2;
  color: white;
  text-align: start;
  max-width: 500px;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(24, 144, 255, 0.2) 0%, rgba(47, 84, 235, 0.15) 100%);
  z-index: 1;
}

.image-content {
  position: relative;
  z-index: 2;
}

.image-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 16px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  line-height: 1.3;
}

.image-subtitle {
  font-size: 14px;
  opacity: 0.9;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  line-height: 1.5;
}

/* 右侧表单区域 */
.auth-right {
  flex: 1;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* 移动端标题（默认隐藏） */
.mobile-header {
  display: none;
  text-align: center;
  margin-bottom: 30px;
}

.mobile-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.mobile-subtitle {
  font-size: 14px;
  color: #666;
}

/* 表单头部 */
.form-header {
  text-align: center;
  margin-bottom: 40px;
}

.form-header h2 {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.form-header p {
  font-size: 14px;
  color: #666;
}

/* 表单样式 */
.auth-form {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}

.form-item {
  margin-bottom: 24px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.remember-checkbox {
  color: #666;
}

.forgot-password {
  font-size: 14px;
}

.submit-button {
  width: 100%;
  padding: 15px;
  font-size: 16px;
  font-weight: 600;
}

.form-switch {
  text-align: center;
  margin-top: 20px;
}

.switch-link {
  font-size: 14px;
}

.form-footer {
  text-align: center;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #e8e8e8;
}

.form-footer p {
  font-size: 12px;
  color: #999;
  margin: 4px 0;
}

/* 移动端优化（最大宽度 768px） */
@media (max-width: 768px) {
  .auth-page {
    padding: 0 16px;
    align-items: flex-start;
    min-height: 100vh;
    background-color: #f9fafb;
  }

  .auth-card {
    border-radius: 16px;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.08);
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .auth-layout {
    flex-direction: column;
    min-height: auto;
  }

  .auth-left {
    display: none;
  }

  .mobile-header {
    display: block;
    text-align: center;
    margin-bottom: 32px;
    padding-top: 24px;
  }

  .mobile-title {
    font-size: 26px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 6px;
    line-height: 1.3;
  }

  .mobile-subtitle {
    font-size: 15px;
    color: #666;
    opacity: 0.9;
  }

  .auth-right {
    padding: 32px 20px 40px;
    background-color: #ffffff;
  }

  /* 表单头部 */
  .form-header {
    text-align: center;
    margin-bottom: 36px;
  }

  .form-header h2 {
    font-size: 24px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 10px;
  }

  .form-header p {
    font-size: 15px;
    color: #777;
    line-height: 1.5;
  }

  /* 表单项 */
  .form-item {
    margin-bottom: 22px;
  }

  .auth-form :deep(.el-input__inner) {
    height: 52px;
    font-size: 16px;
    padding: 0 16px;
  }

  .auth-form :deep(.el-input__prefix) {
    left: 16px;
  }

  .auth-form :deep(.el-input__suffix) {
    right: 16px;
  }

  .form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    flex-wrap: wrap;
    gap: 12px;
  }

  .remember-checkbox :deep(.el-checkbox__label) {
    font-size: 15px;
    color: #555;
  }

  .forgot-password {
    font-size: 15px;
    color: #409eff;
    margin-left: auto;
  }

  /* 提交按钮 */
  .submit-button {
    height: 52px;
    font-size: 17px;
    font-weight: 600;
    letter-spacing: 0.5px;
  }

  /* 切换链接 */
  .form-switch {
    margin-top: 24px;
  }

  .switch-link {
    font-size: 16px;
    color: #409eff;
    font-weight: 500;
  }

  /* 底部版权 */
  .form-footer {
    margin-top: 40px;
    padding-top: 24px;
    border-top: 1px solid #eee;
  }

  .form-footer p {
    font-size: 13px;
    color: #888;
    line-height: 1.6;
  }
}

@media (max-width: 480px) {
  .auth-page {
    padding-top: 20px;
  }
  
  .auth-right {
    padding: 24px 16px;
  }
  
  .mobile-title {
    font-size: 20px;
  }
  
  .form-header h2 {
    font-size: 22px;
  }
  
  .form-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .forgot-password {
    margin-top: 8px;
  }
}

/* 平板设备适配 */
@media (min-width: 769px) and (max-width: 1024px) {
  .auth-container {
    max-width: 800px;
  }
  
  .auth-layout {
    min-height: 500px;
  }
  
  .auth-left {
    padding: 30px;
  }
  
  .image-title {
    font-size: 20px;
  }
  
  .image-subtitle {
    font-size: 12px;
  }
  
  .auth-right {
    padding: 30px;
  }
}
</style>