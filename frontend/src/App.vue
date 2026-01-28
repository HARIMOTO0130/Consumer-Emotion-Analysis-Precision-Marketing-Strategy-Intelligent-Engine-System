<script setup>
import Navbar from './components/Navbar.vue'
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

// 检查当前路由是否为登录页面
const isLoginPage = computed(() => {
  return route.path === '/login'
})
</script>

<template>
  <div class="app-container">
    <!-- 只在非登录页面显示导航栏 -->
    <Navbar v-if="!isLoginPage" class="app-navbar" />
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

html, body {
  width: 100%;
  overflow-x: hidden;
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
  width: 100%;
}

.app-navbar {
  width: 100%;
  position: relative;
}

.app-navbar ::v-deep(.navbar) {
  margin: 0;
  padding: 0;
  width: 100%;
  border-radius: 0;
}

.app-navbar ::v-deep(.navbar-container) {
  max-width: 100%;
  margin: 0;
  padding-left: 0;
  padding-right: 0;
}

/* 在移动端进一步调整 */
@media (max-width: 768px) {
  .app-navbar ::v-deep(.navbar) {
    padding-left: 0;
    padding-right: 0;
  }
  
  .app-navbar ::v-deep(.navbar-container) {
    padding-left: 16px;
    padding-right: 16px;
  }
}

</style>