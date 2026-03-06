import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import Components from 'unplugin-vue-components/vite'
import Icons from 'unplugin-icons/vite'
import IconResolver from 'unplugin-icons/resolver'

import AutoImport from 'unplugin-auto-import/vite';
import { TDesignResolver } from '@tdesign-vue-next/auto-import-resolver';

export default defineConfig({
  plugins: [
    vue(),
    Icons({
      compiler: 'vue3',
      autoInstall: false,
    }),
    AutoImport({
      resolvers: [
        TDesignResolver({
          library: 'vue-next'
        }),
      ],
    }),
    Components({
      dts: true,
      dirs: ['src/components'],
      resolvers: [
        IconResolver({
          prefix: 'i',
          extension: 'vue',
        }),
        TDesignResolver({
          library: 'vue-next'
        }),
      ],
    }),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@views': path.resolve(__dirname, './src/views'),
      '@services': path.resolve(__dirname, './src/services'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@stores': path.resolve(__dirname, './src/store'),
      '@routes': path.resolve(__dirname, './src/router'),
      '@assets': path.resolve(__dirname, './src/assets'),
      '@styles': path.resolve(__dirname, './src/styles'),
    }
  },
  // 实际部署时删除
  server: {
    proxy: {
      '/chat-api': {
        target: process.env.VITE_CHAT_SERVER_API_URL,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/chat-api/, '')
      }
    }
  }
})