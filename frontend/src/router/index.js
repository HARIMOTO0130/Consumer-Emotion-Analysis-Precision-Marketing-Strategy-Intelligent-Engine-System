import { createRouter, createWebHistory } from 'vue-router'
import {useAuthStore} from '@stores/auth.js'
import Dashboard from '../views/Dashboard.vue'
import DataSource from '../views/DataSource.vue'
import MarketingStrategy from '../views/MarketingStrategy.vue'
import Login from '../views/Auth/Login.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    name: 'Home',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/data-source',
    name: 'DataSource',
    component: DataSource,
    meta: { requiresAuth: true }
  },
  {
    path: '/marketing-strategy',
    name: 'MarketingStrategy',
    component: MarketingStrategy,
    meta: { requiresAuth: true }
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ path: '/login', query: { redirect: to.fullPath } })
  } 
  // 如果路由仅游客可访问，但用户已登录 → 跳转到首页
  else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ path: '/' })
  } 
  // 其他情况正常放行
  else {
    next()
  }
})

// 全局后置守卫
router.afterEach((to) => {
  document.title = to.meta.title || '智能营销引擎系统'
})

export default router
