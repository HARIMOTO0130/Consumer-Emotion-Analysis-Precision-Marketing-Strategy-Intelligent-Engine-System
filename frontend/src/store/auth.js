/**
 * @desc:封装的认证相关的Store,用于管理登录状态，使用pinia持久化插件管理持久化
 * @author:jh
 */
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  persist: {
    enabled: true,
    storage:localStorage,
    paths: ['accessToken', 'refreshToken', 'expiresAt', 'name'],
  },

  state: () => ({
    name: null,             // 用户名
    accessToken: null,      // 认证密钥
    refreshToken: null,     // 刷新密钥
    expiresAt: null,        // 过期时间戳（ms）
  }),

  getters: {
    isAuthenticated: (state) => {
      return !!state.accessToken && Date.now() < state.expiresAt
    },
  },

  actions: {
    login(userData) {
      const { name, access_token, refresh_token, expires_in } = userData

      this.name = name
      this.accessToken = access_token
      this.refreshToken = refresh_token
      this.expiresAt = Date.now() + expires_in * 1000
    },

    logout() {
      this.name = null
      this.accessToken = null
      this.refreshToken = null
      this.expiresAt = null
    },
  },
})