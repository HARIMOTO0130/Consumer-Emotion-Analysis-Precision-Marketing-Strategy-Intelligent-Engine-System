import api from "./api";
import { useAuthStore } from "@stores/auth";

/**
 * @desc: 在这里写登录、注册、刷新认证token的逻辑，看你想不想写
 * @author: jh
 */

/**
 * 这里假设login接口返回
 * @param status(boolean): 响应是否成功
 * @param msg(string): message
 * @param name: 用户名
 * @param access_token,refresh_token,expires_in 我也不爱写jwt认证逻辑，这里暂时不用
 */
export const login = async (username, password) => {
  try {
    // fake_data
    if (username === 'admin' && password === 'admin123') {
      const authStore = useAuthStore()
      authStore.login({ 
        name: username, 
        access_token: 'fake_access_token_123456', 
        refresh_token: 'fake_refresh_token_123456', 
        expires_in: 3600 
      })
      return {
        status: true,
        msg: '登录成功'
      }
    }

    const response = await api.post('/login', {
      user_name: username,
      pwsd: password
    });

    const { name, access_token, refresh_token, expires_in } = response.data

    // 更新 AuthStore
    const authStore = useAuthStore()
    authStore.login({ name, access_token, refresh_token, expires_in })
    return { status: true, msg: '登录成功' }
  } catch (error) {
    const msg = error.response?.data?.msg || '登录失败，请检查账号密码'
    return { status: false, msg }
  }
}

export const register = async (username, password) => {
  try {
    // fake_data
    if (username === 'admin' && password === 'admin123') {
      const authStore = useAuthStore()
      authStore.login({ 
        name: username, 
        access_token: 'fake_access_token_123456', 
        refresh_token: 'fake_refresh_token_123456', 
        expires_in: 3600 
      })
      return {
        status: true,
        msg: '注册成功'
      }
    }
    const response = await api.post('/register', {
      user_name: username,
      pwsd: password
    })

    const { name, access_token, refresh_token, expires_in } = response.data

    const authStore = useAuthStore();
    authStore.login({ name, access_token, refresh_token, expires_in })

    return { status: true, msg: '注册成功' }
  } catch (error) {
    const msg = error.response?.data?.msg || '注册失败'
    return { status: false, msg }
  }
}

// 保留
export const refreshToken = async () => {
  try {
    // fake_data
    return {
      status: true,
      access_token: 'fake_new_access_token_654321',
      refresh_token: 'fake_new_refresh_token_654321',
      expires_in: 3600
    }

    const authStore = useAuthStore()
    const response = await api.post('/refresh-token', {
      refresh_token: authStore.refresh_token
    })
    const { access_token, refresh_token, expires_in } = response.data
    authStore.updateToken({ access_token, refresh_token, expires_in })
    return { status: true }
  } catch (error) {
    const msg = error.response?.data?.msg || 'Token刷新失败，请重新登录'
    return { status: false, msg }
  }
}