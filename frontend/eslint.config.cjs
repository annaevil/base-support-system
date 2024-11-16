// eslint.config.cjs
module.exports = {
    extends: [
      'plugin:vue/vue3-recommended',
      'plugin:@typescript-eslint/recommended',
      'plugin:vuejs-accessibility/recommended',
      'eslint:recommended',
      'plugin:import/recommended',
      'plugin:sonarjs/recommended-legacy',
      'prettier',
    ],
    plugins: ['vue', 'vuejs-accessibility', 'import', 'sonarjs'],
    parser: '@babel/eslint-parser',
    parserOptions: {
      ecmaVersion: 2022,
      requireConfigFile: false,
      sourceType: 'module',
    },
    rules: {
      semi: 'error',
      'prefer-const': 'error',
      'vuejs-accessibility/click-events-have-key-events': 'off',
      'vuejs-accessibility/form-control-has-label': 'off',
      'vuejs-accessibility/mouse-events-have-key-events': 'off',
      'vuejs-accessibility/no-static-element-interactions': 'off',
    },
    overrides: [
      {
        files: ['**/*.ts', '**/*.tsx', '**/*.vue'],
      },
    ],
  };
  