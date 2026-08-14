import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import { resolve } from "node:path";

export default defineConfig({
  root: resolve(__dirname, "frontend"),
  publicDir: resolve(__dirname, "public"),
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    port: 4173,
    proxy: {
      "/api": "http://127.0.0.1:8765",
    },
  },
  build: {
    outDir: resolve(__dirname, "frontend_dist"),
    emptyOutDir: true,
    sourcemap: false,
    target: "es2020",
  },
});
