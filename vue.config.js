const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  chainWebpack: config => {
    config
        .plugin('html')
        .tap(args => {
          args[0].title= 'ECUST-内网门户系统'
          return args
        })
  }
})
