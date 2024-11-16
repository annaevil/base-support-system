import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import svgLoader from 'vite-svg-loader'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    svgLoader(),
    AutoImport({
      imports: [
        {
          '@vuelidate/core': ['useVuelidate'],
          '@vuelidate/validators': [
            'required',
            'minLength',
            'maxLength',
            'email',
            'helpers'
          ],
        },
        {
          '@/plugins/vuelidate/validation-rules': [
            'requiredRule',
            'minLengthRule',
            'maxLengthRule',
            'emailRule'
          ],
        },
        {
          '@/plugins/use-password-visibility': [
            'usePasswordVisibility',
          ],
        },
        {
          '@/utils/token': [
            'setAuthToken',
            'getAuthToken',
            'removeAuthToken',
          ],
        },
      ],
      dts: './src/auto-imports.d.ts',
    }),
  ],
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `
      @import "@/styles/_variables.scss";
      @import "@/styles/main.scss";
    `,
      },
    },
  },
  resolve: {
    alias: {
      '@': '/src',
      '&': '/srс/components',
      '#': '/public',
    },
  },
  server: {
    watch: {
      usePolling: true,
    },
    host: true,
    strictPort: true,
    port: 3005,
  },
})
