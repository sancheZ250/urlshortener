import { defineConfig } from 'vite';
import Vue from '@vitejs/plugin-vue';
// import { createProxyMiddleware } from 'http-proxy-middleware';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [Vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://backend:8000', //адрес бэкенда
        changeOrigin: true,
      },
      '/auth':{
        target: 'http://backend:8000',
        changeOrigin: true,
      },
      },
    },
  },
);