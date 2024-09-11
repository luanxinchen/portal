import { createRouter, createWebHistory } from 'vue-router'
import {ElMessage} from 'element-plus';

const routes = [
  {
    path: '',
    redirect: {name: 'Portal'}
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: {
      title: '登录'
    }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  // to 即将访问的路由对象
  // from 当前正要离开的路由对象
  // next() 继续向后执行
  // next(false) 中断导航，保持当前界面
  // next("xxx") 跳转到对象
  // 更新动态标题
  if (to.meta.title == undefined) {
    document.title = 'ECUST'
  } else {
    document.title = to.meta.title + '-ECUST'
  }

  let token = localStorage.getItem('token')
  if (token) {
    // 已登录
    next();
    return
  }

  // 未登录，允许访问登录页面
  const allowedRoutes = ["Login", "Portal"];
  if (allowedRoutes.includes(to.name)) {
    next();
    return;
  }
  // 未登录，强制跳转登录页面
  next({name: "Login"});
  ElMessage.warning("请登录后访问")

})

export default router
