import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "http://localhost:8080/api/v1/openapi.json",
  output: {
    path: "./src/client",
    clean: true,
    postProcess: ["eslint"],
  },
  plugins: [
    {
      name: "@hey-api/sdk",
      validator: {
        request: false,
        response: true,
      },
    },
    "@hey-api/typescript",
    "@hey-api/client-axios",
    "@tanstack/react-query",
    "zod",
  ],
});
