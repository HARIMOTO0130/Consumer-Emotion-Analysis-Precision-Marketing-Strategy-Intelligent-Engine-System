import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import TDesignChat from '@tdesign-vue-next/chat';
import 'tdesign-vue-next/es/style/index.css';

// 这里引入animate.css,简化动画使用
import 'animate.css';
// 引入自定义颜色常量，用于统一颜色
import '@styles/variables.css'
// 全局引用封装好的iconfy-icon组件
import mdicon from '@/components/mdicon.vue'
// 创建Pinia实例
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

// 创建App实例
const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.use(TDesignChat)
// 注册为全局组件
app.component('mdicon', mdicon)
// 全局注册el-icon，这样El-input的prefix-icon才会显示
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component);
}

app.use(pinia);
app.mount('#app')