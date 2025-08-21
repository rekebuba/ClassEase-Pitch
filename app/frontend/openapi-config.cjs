/** @type {import('@rtk-query/codegen-openapi').ConfigFile} */
module.exports = {
  schemaFile: "http://backend:8000/api/v1/openapi.json",
  apiFile: "./src/store/base-api.ts",
  apiImport: "baseApi",
  outputFile: "./src/store/api.ts",
  exportName: "api",
  hooks: true,
};
