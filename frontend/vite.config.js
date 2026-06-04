import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5174,
    strictPort: true,
  },
  // Vercel 배포 시 정적 파일 위치 지정
  base: '/',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
})
