module.exports = {
    parser: '@typescript-eslint/parser',
    parserOptions: {
      ecmaVersion: 2021,
      sourceType: 'module',
      ecmaFeatures: {
        jsx: true
      },
      project: './tsconfig.json' // enable if using type-aware linting
    },
    env: {
      browser: true,
      es2021: true,
      node: true
    },
    extends: [
      'eslint:recommended',
      'plugin:@typescript-eslint/recommended',
      'plugin:react/recommended',
      'plugin:react-hooks/recommended',
      'react-app',
      'react-app/jest',
      'prettier' // ✨ optional: disable formatting rules if using Prettier
    ],
    plugins: ['@typescript-eslint', 'react', 'react-hooks'],
    rules: {
      // React
      'react/react-in-jsx-scope': 'off',
      'react/prop-types': 'off',
      'react/jsx-pascal-case': 'error',
      'react/jsx-no-duplicate-props': 'error',
  
      // React Hooks
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
  
      // TypeScript
      '@typescript-eslint/explicit-module-boundary-types': 'off',
      '@typescript-eslint/no-explicit-any': 'warn',
  
      // General JavaScript
      'no-unused-vars': 'warn',
      'eqeqeq': 'warn',
      'semi': ['error', 'always']
    },
    settings: {
      react: {
        version: 'detect'
      }
    }
  };
