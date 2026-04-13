import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // 适配GitHub Pages的路径
  base: '/resume-analyzer/',
  server: {
    port: 5173,
    host: true
  }
})
