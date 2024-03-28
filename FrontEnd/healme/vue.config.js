const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({  
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:8100/', // Target backend or Kong API gateway
        changeOrigin: true, // Necessary for virtual hosted sites, this changes the origin of the host header to the target URL
        pathRewrite: { '^/api': '' }, // Rewrite the path: remove `/api` prefix when forwarding the request
      },
    },
  },
  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}
  }
})
