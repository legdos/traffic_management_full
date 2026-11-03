import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// 后端地址：与 traffic_management_backend/src/main/resources/application.yaml 的 server.port 保持一致
const BACKEND_TARGET = 'http://localhost:8080'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      // Windows 下 URL.pathname 会得到 "/D:/..."，必须用 fileURLToPath 转成盘符路径
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5173,
    proxy: {
      // 工厂接口转发
      '/factories': {
        target: BACKEND_TARGET,
        changeOrigin: true,
      },
      // 车辆接口转发
      '/vehicles': {
        target: BACKEND_TARGET,
        changeOrigin: true,
      },
      // 需求接口转发
      '/needs': {
        target: BACKEND_TARGET,
        changeOrigin: true,
      },
      // 任务/订单接口转发
      '/missions': {
        target: BACKEND_TARGET,
        changeOrigin: true,
      },
      // 路线折线接口转发
      '/routes': {
        target: BACKEND_TARGET,
        changeOrigin: true,
      },
      // 仿真控制接口转发
      '/sim': {
        target: BACKEND_TARGET,
        changeOrigin: true,
      },
    },
  },
})
