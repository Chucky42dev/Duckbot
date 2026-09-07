import { defineConfig } from "vite";

// Modely se berou přímo z ../model, žádné kopírování.
export default defineConfig({
  publicDir: "../model",
  base: "./",
  server: { port: 5180, open: false },
  build: { outDir: "dist", emptyOutDir: true, target: "esnext" },
  optimizeDeps: { exclude: ["@mujoco/mujoco"] },
});
