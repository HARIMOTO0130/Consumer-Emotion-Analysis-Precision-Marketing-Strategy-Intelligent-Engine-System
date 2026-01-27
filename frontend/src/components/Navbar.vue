<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isMobileMenuOpen = ref(false)

const handleLogout = () => {
  console.log('退出登录')
  router.push('/login')
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}
</script>

<template>
  <nav class="navbar">
    <!-- 品牌标识 -->
    <div class="navbar-brand">
      <h1 class="brand-title">
        🎯 消费者情感分析与精准营销策略的智能引擎
      </h1>
      <p class="brand-subtitle">
        Consumer Emotion Analysis & Precision Marketing Strategy Intelligent Engine System
      </p>
    </div>
    
    <!-- 桌面端导航菜单 -->
    <div class="navbar-menu">
      <router-link to="/" class="nav-item">情感分析仪表盘</router-link>
      <router-link to="/data-source" class="nav-item">数据源管理</router-link>
      <router-link to="/marketing-strategy" class="nav-item">营销策略推荐</router-link>
    </div>
    
    <!-- 用户操作 -->
    <div class="navbar-actions">
      <div class="user-info">
        <span class="user-name">管理员</span>
        <span class="user-role">系统管理员</span>
      </div>
      <button class="btn-logout" @click="handleLogout">退出</button>
    </div>
    
    <!-- 移动端菜单按钮 -->
    <button class="mobile-menu-btn" @click="toggleMobileMenu">
      <span class="menu-icon"></span>
      <span class="menu-icon"></span>
      <span class="menu-icon"></span>
    </button>
  </nav>
  
  <!-- 移动端导航菜单 -->
  <div class="mobile-menu" :class="{ 'open': isMobileMenuOpen }">
    <div class="mobile-menu-content">
      <router-link to="/" class="mobile-nav-item" @click="isMobileMenuOpen = false">情感分析仪表盘</router-link>
      <router-link to="/data-source" class="mobile-nav-item" @click="isMobileMenuOpen = false">数据源管理</router-link>
      <router-link to="/marketing-strategy" class="mobile-nav-item" @click="isMobileMenuOpen = false">营销策略推荐</router-link>
      <div class="mobile-user-info">
        <span class="user-name">管理员</span>
        <button class="mobile-btn-logout" @click="handleLogout">退出</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px 40px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
  position: relative;
  z-index: 1000;
}

.navbar-brand {
  flex: 1;
  min-width: 200px;
}

.brand-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 5px;
  line-height: 1.2;
}

.brand-subtitle {
  font-size: 0.875rem;
  opacity: 0.9;
  margin: 0;
}

.navbar-menu {
  display: flex;
  gap: 15px;
  align-items: center;
}

.nav-item {
  color: white;
  text-decoration: none;
  padding: 10px 15px;
  border-radius: 4px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 5px;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.nav-item.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
  font-weight: bold;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  text-align: right;
}

.user-name {
  display: block;
  font-weight: bold;
  margin-bottom: 2px;
}

.user-role {
  display: block;
  font-size: 0.875rem;
  opacity: 0.9;
}

.btn-logout {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-logout:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

/* 移动端菜单按钮 */
.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 10px;
}

.menu-icon {
  display: block;
  width: 24px;
  height: 3px;
  background-color: white;
  margin: 5px 0;
  transition: all 0.3s ease;
}

/* 移动端导航菜单 */
.mobile-menu {
  position: fixed;
  top: 0;
  right: -100%;
  width: 80%;
  max-width: 300px;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: -4px 0 6px rgba(0, 0, 0, 0.1);
  transition: right 0.3s ease;
  z-index: 999;
  padding: 40px 20px;
}

.mobile-menu.open {
  right: 0;
}

.mobile-menu-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

.mobile-nav-item {
  color: white;
  text-decoration: none;
  padding: 15px 20px;
  border-radius: 4px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.mobile-nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.mobile-user-info {
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.mobile-btn-logout {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mobile-btn-logout:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

/* 响应式适配 */
@media (max-width: 1200px) {
  .navbar {
    padding: 15px 30px;
  }
  
  .brand-title {
    font-size: 1.25rem;
  }
  
  .brand-subtitle {
    font-size: 0.75rem;
  }
  
  .nav-item {
    padding: 8px 12px;
    font-size: 0.875rem;
  }
}

@media (max-width: 992px) {
  .navbar-brand {
    min-width: 150px;
  }
  
  .brand-title {
    font-size: 1.125rem;
  }
  
  .navbar-menu {
    gap: 10px;
  }
  
  .navbar-actions {
    gap: 15px;
  }
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
    padding: 15px 20px;
  }
  
  .navbar-brand {
    text-align: center;
  }
  
  .navbar-menu {
    justify-content: center;
  }
  
  .navbar-actions {
    justify-content: space-between;
  }
  
  .user-info {
    text-align: left;
  }
}

@media (max-width: 576px) {
  .navbar-menu {
    display: none;
  }
  
  .navbar-actions {
    display: none;
  }
  
  .mobile-menu-btn {
    display: block;
    position: absolute;
    top: 20px;
    right: 20px;
  }
  
  .navbar-brand {
    margin-right: 60px;
  }
  
  .brand-title {
    font-size: 1rem;
  }
  
  .brand-subtitle {
    font-size: 0.625rem;
  }
}
</style>