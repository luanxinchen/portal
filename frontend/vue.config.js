const {defineConfig} = require('@vue/cli-service')
module.exports = defineConfig({
    devServer: {
        client: {
            overlay: false
        }
    },
    transpileDependencies: true,
    lintOnSave: false,
    chainWebpack: config => {
        config
            .plugin('html')
            .tap(args => {
                args[0].title = 'ECUST-内网门户系统'
                return args
            })
    }
})
