<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@stores/auth.js'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()
const isMobileMenuOpen = ref(false)

const handleLogout = () => {
  authStore.logout()
  ElMessage.success('已成功退出登录！')
  router.push('/login')
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}
</script>

<template>
  <div>
    <nav class="navbar">
      <div class="navbar-container">
        <!-- 品牌区域 -->
        <div class="navbar-brand">
          <h1 class="brand-title">
            知湘知味
          </h1>
        </div>
        
        <!-- 桌面端导航菜单 -->
        <div class="navbar-desktop-menu">
          <router-link to="/" class="nav-item" :class="{ 'active': $route.path === '/' }">
            情感分析仪表盘
          </router-link>
          <router-link to="/data-source" class="nav-item" :class="{ 'active': $route.path === '/data-source' }">
            数据源管理
          </router-link>
          <router-link to="/marketing-strategy" class="nav-item" :class="{ 'active': $route.path === '/marketing-strategy' }">
            营销策略推荐
          </router-link>
        </div>
        
        <!-- 桌面端用户操作 -->
        <div class="navbar-desktop-actions">
          <div class="user-info">
            <span class="user-name">{{ authStore.name || '管理员' }}</span>
            <span class="user-role">系统管理员</span>
          </div>
          <button class="btn-logout" @click="handleLogout">
            退出
          </button>
        </div>
        
        <!-- 移动端菜单按钮 -->
        <button class="mobile-menu-btn" @click="toggleMobileMenu" :aria-expanded="isMobileMenuOpen">
          <div class="menu-icon-wrapper">
            <span class="menu-icon" :class="{ 'open': isMobileMenuOpen }"></span>
            <span class="menu-icon" :class="{ 'open': isMobileMenuOpen }"></span>
            <span class="menu-icon" :class="{ 'open': isMobileMenuOpen }"></span>
          </div>
        </button>
      </div>
    </nav>
    
    <!-- 移动端侧滑菜单 -->
    <div class="mobile-menu-overlay" :class="{ 'open': isMobileMenuOpen }" @click="toggleMobileMenu"></div>
    <div class="mobile-menu" :class="{ 'open': isMobileMenuOpen }">
      <div class="mobile-menu-header">
        <div class="mobile-user-info">
          <div class="user-avatar">
            <span class="avatar-text">{{ authStore.name?.charAt(0) || 'A' }}</span>
          </div>
          <div class="user-details">
            <span class="user-name">{{ authStore.name || '管理员' }}</span>
            <span class="user-role">系统管理员</span>
          </div>
        </div>
        <button class="mobile-close-btn" @click="toggleMobileMenu">
          <mdicon name="close" color="white"/>
        </button>
      </div>
      
      <div class="mobile-menu-content">
        <router-link 
          to="/" 
          class="mobile-nav-item" 
          :class="{ 'active': $route.path === '/' }"
          @click="toggleMobileMenu"
        >
          <span>情感分析仪表盘</span>
        </router-link>
        <router-link 
          to="/data-source" 
          class="mobile-nav-item"
          :class="{ 'active': $route.path === '/data-source' }"
          @click="toggleMobileMenu"
        >
          <span>数据源管理</span>
        </router-link>
        <router-link 
          to="/marketing-strategy" 
          class="mobile-nav-item"
          :class="{ 'active': $route.path === '/marketing-strategy' }"
          @click="toggleMobileMenu"
        >
          <span>营销策略推荐</span>
        </router-link>
      </div>
      
      <div class="mobile-menu-footer">
        <button class="mobile-btn-logout" @click="handleLogout">
          退出登录
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 基础样式重置 */
* {
  box-sizing: border-box;
}

/* 导航栏容器 */
.navbar {
  background-color: var(--color-primary);
  color: white;
  position: relative;
  z-index: 1000;
  width: 100%;
}

.navbar-container {
  max-width: 1440px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  position: relative;
}

/* 品牌区域 */
.navbar-brand {
  flex: 1;
  min-width: 0;
  justify-items: start;
  max-width: 400px;
}

.brand-title {
  font-size: 1.4rem;
  font-weight: 800;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.brand-subtitle {
  font-size: 0.75rem;
  opacity: 0.9;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 桌面端导航菜单 */
.navbar-desktop-menu {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-shrink: 0;
}

.nav-item {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

.nav-item.active {
  background-color: rgba(255, 255, 255, 0.25);
  font-weight: 600;
}

/* 桌面端用户操作 */
.navbar-desktop-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;
}

.user-info {
  text-align: right;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-weight: 600;
  font-size: 0.95rem;
}

.user-role {
  font-size: 0.8rem;
  opacity: 0.9;
}

.btn-logout {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn-logout:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

/* 移动端菜单按钮 */
.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  margin-left: auto;
  position: relative;
  z-index: 1001;
}

.menu-icon-wrapper {
  width: 24px;
  height: 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}

.menu-icon {
  display: block;
  width: 20px;
  height: 2px;
  background-color: white;
  border-radius: 1px;
  transition: all 0.3s ease;
}

.menu-icon:nth-child(1) {
  transform-origin: center;
}

.menu-icon:nth-child(2) {
  opacity: 1;
}

.menu-icon:nth-child(3) {
  transform-origin: center;
}

.menu-icon.open:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.menu-icon.open:nth-child(2) {
  opacity: 0;
}

.menu-icon.open:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

/* 移动端菜单遮罩 */
.mobile-menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.mobile-menu-overlay.open {
  opacity: 1;
  visibility: visible;
}

/* 移动端侧滑菜单 */
.mobile-menu {
  position: fixed;
  top: 0;
  right: -320px;
  width: 300px;
  height: 100vh;
  background: white;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.15);
  transition: right 0.3s ease;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.mobile-menu.open {
  right: 0;
}

.mobile-menu-header {
  background-color: var(--color-primary);
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.mobile-user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-text {
  font-size: 1.2rem;
  font-weight: 600;
  color: white;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.mobile-menu-header .user-name {
  font-size: 1rem;
  color: white;
}

.mobile-menu-header .user-role {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.9);
}

.mobile-close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.mobile-menu-content {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
}

.mobile-nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  color: #333;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.2s ease;
  border-left: 4px solid transparent;
}

.mobile-nav-item.active {
  background-color: #f0f4ff;
  border-left-color: var(--color-primary);
  color: var(--color-primary);
}

.nav-icon {
  font-size: 1.2rem;
  width: 24px;
  text-align: center;
}

.mobile-menu-footer {
  padding: 20px;
  border-top: 1px solid #e0e0e0;
}

.mobile-btn-logout {
  width: 100%;
  background-color: var(--color-danger);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.mobile-btn-logout:hover {
  opacity: 0.9;
  background-color: var(--color-danger-hover);
}

.logout-icon {
  font-size: 1.1rem;
}

/* 响应式设计 */
@media (max-width: 1100px) {
  .navbar-container {
    padding: 16px 20px;
    gap: 20px;
  }
  
  .brand-title {
    font-size: 1.15rem;
  }
  
  .brand-subtitle {
    font-size: 0.7rem;
  }
  
  .nav-item {
    padding: 8px 12px;
    font-size: 0.9rem;
  }
  
  .btn-logout {
    padding: 8px 12px;
    font-size: 0.9rem;
  }
}

@media (max-width: 900px) {
  .navbar-container {
    padding: 14px 16px;
    gap: 16px;
  }
  
  .navbar-brand {
    max-width: 300px;
  }
  
  .brand-title {
    font-size: 1.05rem;
  }
  
  .brand-subtitle {
    font-size: 0.65rem;
  }
  
  .navbar-desktop-menu {
    gap: 4px;
  }
  
  .nav-item {
    padding: 6px 10px;
    font-size: 0.85rem;
  }
  
  .navbar-desktop-actions {
    gap: 12px;
  }
  
  .user-name {
    font-size: 0.9rem;
  }
  
  .user-role {
    font-size: 0.75rem;
  }
}

@media (max-width: 768px) {
  .navbar-desktop-menu,
  .navbar-desktop-actions {
    display: none;
  }
  
  .mobile-menu-btn {
    display: block;
  }
  
  .navbar-container {
    padding: 12px 16px;
  }
  
  .navbar-brand {
    max-width: calc(100% - 60px)
  }
  
  .brand-title {
    font-size: 1rem;
    white-space: normal;
    line-height: 1.2;
  }
  
  .brand-subtitle {
    display: none;
  }
}

@media (max-width: 480px) {
  .navbar-container {
    padding: 10px 12px;
  }
  
  .brand-title {
    font-size: 0.9rem;
  }
  
  .mobile-menu {
    width: 280px;
  }
  
  .mobile-menu-header {
    padding: 16px;
  }
  
  .mobile-nav-item {
    padding: 14px 20px;
    font-size: 0.95rem;
  }
}
</style>