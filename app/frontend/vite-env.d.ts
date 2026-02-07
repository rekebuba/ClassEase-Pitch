/// <reference types="vite-plugin-svgr/client" />

type ImportMetaEnv = {
  readonly VITE_API_BASE_URL: string;
};

type ImportMeta = {
  readonly env: ImportMetaEnv;
};
