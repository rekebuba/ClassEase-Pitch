// eslint.config.js
import tsPlugin from "@typescript-eslint/eslint-plugin";
import parser from "@typescript-eslint/parser";
import jsxA11y from "eslint-plugin-jsx-a11y";
import prettier from "eslint-plugin-prettier";
import reactPlugin from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";

export default [
  {
    files: ["**/*.{ts,tsx,js,jsx}"],
    languageOptions: {
      parser,
      ecmaVersion: "latest",
      sourceType: "module",
    },
    plugins: {
      "@typescript-eslint": tsPlugin,
      react: reactPlugin,
      "react-hooks": reactHooks,
      "jsx-a11y": jsxA11y,
      prettier: prettier,
    },
    rules: {
      "prettier/prettier": "warn",
      "react/react-in-jsx-scope": "off",
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_", vars: "all", varsIgnorePattern: "^_" },
      ],
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",
      eqeqeq: "warn",
      semi: ["error", "always"],
    },
    settings: {
      react: { version: "detect" },
    },
  },
];
