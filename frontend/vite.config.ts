import { fileURLToPath, URL } from 'node:url'

/// <reference types="vitest" />
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
    plugins: [vue(), vueDevTools(), tailwindcss()],
    test: {
        globals: true, // so you can use `test`, `expect`, etc. without imports
        environment: "jsdom", // simulate browser
        setupFiles: "./src/setupTests.ts", // optional file for setup like jest-dom
    },
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url)),
        },
    },
    server: {
        host: '0.0.0.0',
        port: 5173,
        allowedHosts: [
          'localhost',
          'shrew-precise-wrongly.ngrok-free.app',
          '*.ngrok-free.app',
        ],
      },
});
