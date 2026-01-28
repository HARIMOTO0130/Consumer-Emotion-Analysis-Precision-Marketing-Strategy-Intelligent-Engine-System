/**
 * @desc：封装axios，在此修改全局请求拦截器与相应拦截器
 * @author：jh
 */
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_SERVER_API_ENDPOINT || "http://localhost:8000",
  timeout: 10000,
})

// 请求拦截器
api.interceptors.request.use((config) => {
  // 如果需要使用jwt的话可以加上
  // const token = localStorage.getItem('jwt_token')
  // if (token) {
  //   config.headers.Authorization = `Bearer  $ {token}`
  // }
  return config
})

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 403) {
        // 在此编写认证错误的逻辑，如刷新认证密钥，跳转至认证无效页面
    }
    return Promise.reject(error)
  }
)

export default api