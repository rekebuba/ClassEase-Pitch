module.exports = {
    env: {
        browser: true,
        es2021: true,
        node: true
    },
    extends: [
        'eslint:recommended',
        'plugin:react/recommended',
        'plugin:react-hooks/recommended',
        'prettier'
    ],
    parserOptions: {
        ecmaFeatures: {
            jsx: true
        },
        ecmaVersion: 12,
        sourceType: 'module'
    },
    plugins: ['react', 'react-hooks'],
    rules: {
        'react/prop-types': 'off', // You can disable prop-types if not needed
        'react/jsx-no-duplicate-props': 'error',
        // 'react/no-uncontrolled-components': 'error', // Enforce controlled components with onChange
        'react/jsx-uses-react': 'off', // React import is not necessary with React 17+
        'react/react-in-jsx-scope': 'off', // Not necessary with React 17+
        'react/jsx-pascal-case': 'error',
        // 'prettier/prettier': 'error', // Use Prettier formatting rules
        'no-unused-vars': 'warn', // Warn on unused variables
        'eqeqeq': 'warn', // Enforce strict equality (===)
        'semi': ['error', 'always'], // Enforce semicolons
    },
    settings: {
        react: {
            version: 'detect'
        }
    }
};
