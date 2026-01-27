import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import DataSource from '../views/DataSource.vue'
import MarketingStrategy from '../views/MarketingStrategy.vue'
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/data-source',
    name: 'DataSource',
    component: DataSource
  },
  {
    path: '/marketing-strategy',
    name: 'MarketingStrategy',
    component: MarketingStrategy
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
