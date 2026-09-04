import { resolve } from 'path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: { proxy: { '/api': 'http://localhost:3001' } },
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        chatLab: resolve(__dirname, 'chat-lab.html'),
      },
    },
  },
})
