<script setup>
import Navbar from './components/Navbar.vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// 检查当前路由是否为登录页面
const isLoginPage = computed(() => {
  return route.path === '/login'
})

import { computed } from 'vue'
</script>

<template>
  <div class="app-container">
    <!-- 只在非登录页面显示导航栏 -->
    <Navbar v-if="!isLoginPage" />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f5f5;
  color: #333;
  line-height: 1.6;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 30px;
  background-color: #f5f7fa;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .main-content {
    padding: 20px;
  }
}

@media (max-width: 576px) {
  .main-content {
    padding: 15px;
  }
}
</style>
