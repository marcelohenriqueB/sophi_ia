import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from "@tailwindcss/vite";

export default defineConfig(() => ({
  plugins: [vue(), tailwindcss()],

  server: {
    port: 5173,
    strictPort: true,
  },

  base: '/',

  build: {
    outDir: '../static/dist',
    emptyOutDir: true,
    manifest: true,
  },
}))
