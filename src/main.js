// import './plugins/axios'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import {installAxios} from "@/plugins/axios";
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'dayjs/locale/zh-cn' //中文
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
// 引入axios
const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
installAxios(app)
app.use(ElementPlus,{zhCn}).use(store).use(router).mount('#app')
