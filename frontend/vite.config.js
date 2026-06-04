import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5174,
    strictPort: true,
  },
  // GitHub Pages 배포 시 저장소 이름과 동일한 경로 설정 필수
  base: '/PLCO/',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
})
