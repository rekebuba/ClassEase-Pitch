import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "http://backend:8000/api/v1/openapi.json",
  output: {
    path: "./src/client",
    clean: true,
  },
  plugins: [
    {
      name: "@hey-api/sdk",
      validator: true,
    },
    "@hey-api/typescript",
    "@hey-api/client-axios",
    "@tanstack/react-query",
    "zod",
  ],
});
