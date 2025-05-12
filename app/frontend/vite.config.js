import path from "path"
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import svgr from 'vite-plugin-svgr';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(),
  svgr({
    exportAsDefault: false, // this allows named import as ReactComponent
  }),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    }
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    open: true,
    watch: {
      usePolling: true,
    },
  },
})
