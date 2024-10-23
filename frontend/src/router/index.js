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
  {
    path: '/portal',
    name: 'Index',
    component: () => import('../views/user_interface/LayoutView.vue'),
    meta: {
      title: '门户'
    },
    children: [
      {
        path: '',
        name: 'Portal',
        component: () => import('../views/user_interface/PortalView.vue'),
        meta: {
          title: '门户页'
        }
      }
    ]
  },
  {
    path: '/admin',
    name: 'Admin',
    redirect: {name: 'Site'},
    component: () => import('../views/admin_interface/FrontView.vue'),
    meta: {
      title: '首页'
    },
    children: [
      {
        path: 'site',
        name: 'Site',
        component: () => import('@/views/admin_interface/portal/SiteView.vue'),
        meta: {
          title: '站点管理'
        }
      },
      {
        path: 'site_catagory',
        name: 'SiteCategory',
        component: () => import('@/views/admin_interface/portal/SiteCategoryView.vue'),
        meta: {
          title: '站点分类'
        }
      },
      {
        path: 'contract',
        name: 'Contract',
        component: () => import('@/views/admin_interface/portal/ContractView.vue'),
        meta: {
          title: '职能管理'
        }
      },
      {
        path: 'contract_catagory',
        name: 'ContractCategory',
        component: () => import('@/views/admin_interface/portal/ContractCategoryView.vue'),
        meta: {
          title: '职能分类'
        }
      },
      {
        path: 'notify',
        name: 'Notify',
        component: () => import('@/views/admin_interface/portal/NotifyView.vue'),
        meta: {
          title: '通知管理'
        }
      },
      {
        path: 'user',
        name: 'User',
        component: () => import('../views/admin_interface/user/UserView.vue'),
        meta: {
          title: '用户管理'
        }
      },
    ]
  }
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
