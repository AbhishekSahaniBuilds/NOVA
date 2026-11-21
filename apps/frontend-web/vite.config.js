import react from "@vitejs/plugin-react";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";

const currentDirectory = dirname(fileURLToPath(import.meta.url));
const novaRoot = resolve(currentDirectory, "../../");

export default defineConfig({
  plugins: [react()],
  server: {
    fs: {
      allow: [novaRoot],
    },
  },
});
