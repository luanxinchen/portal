<template>
  <div class="main">
    <el-header height="72px" style="border-bottom: 1px solid #e5e6eb">
      <el-row class="pg-header" justify="space-between">
        <div class="logo-title-container">
          <div class="logo">
            <router-link :to="{name:'Site'}">
              <img src="../../assets/ECUST_logo_blue.png" alt="logo">
            </router-link>
          </div>
          <div>
            <h3>ECUST-门户管理后台</h3>
          </div>
        </div>
        <div class="top-menu">
          <el-dropdown>
            <div class="el-dropdown-link">
              <el-icon style="margin: 0 5px">
                <User/>
              </el-icon>
              <span style="margin-right: 5px">{{ name }}</span>
              <el-tag effect="plain" :type="role === '1' ? 'primary' : 'info'">
            {{ role === '1' ? '超级管理员' : '网站管理员' }}
          </el-tag>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="doLogout">注销登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-row>
    </el-header>
    <el-container style="height: 100%">

      <el-aside width="200px">
        <el-scrollbar>
          <div style="width: 180px;margin: 5px 10px">
            <el-menu :default-active="activeRouter" :router="true" :default-openeds="['Portal','User']">
              <el-sub-menu index="Portal">
                <template #title>
                  <el-icon>
                    <Compass/>
                  </el-icon>
                  <span>门户管理</span>
                </template>
                <el-menu-item-group title="站点导航">
                  <el-menu-item index="Site" :route="{name:'Site'}">站点管理</el-menu-item>
                  <el-menu-item v-if="isSuperUser" index="SiteCategory" :route="{name:'SiteCategory'}">站点类别
                  </el-menu-item>
                </el-menu-item-group>
                <el-menu-item-group v-if="isSuperUser" title="职能引导">
                  <el-menu-item index="Contract" :route="{name:'Contract'}">职能管理</el-menu-item>
                  <el-menu-item index="ContractCategory" :route="{name:'ContractCategory'}">职能类别</el-menu-item>
                </el-menu-item-group>
                <el-menu-item-group v-if="isSuperUser" title="通知">
                  <el-menu-item index="Notify" :route="{name:'Notify'}">通知发布</el-menu-item>
                </el-menu-item-group>
              </el-sub-menu>
              <el-sub-menu v-if="isSuperUser" index="User">
                <template #title>
                  <el-icon>
                    <User/>
                  </el-icon>
                  <span>组织架构</span>
                </template>
                <el-menu-item index="User" :route="{name:'User'}">人员管理</el-menu-item>
              </el-sub-menu>
            </el-menu>
          </div>
        </el-scrollbar>
      </el-aside>
      <el-container>
        <el-main>
          <el-scrollbar>
            <el-breadcrumb separator="/" style="padding: 15px 0 15px 25px">
              <el-breadcrumb-item v-for="breadcrumb in breadcrumbs" :key="breadcrumb.to">
                <router-link :to="breadcrumb.to">{{ breadcrumb.label }}</router-link>
              </el-breadcrumb-item>
            </el-breadcrumb>
            <router-view></router-view>
          </el-scrollbar>
        </el-main>
        <el-footer class="custom-footer" height="25px">
          <div class="footer-text">
            <p style="margin: 5px 0 0 0">© 2024 <strong>ECUST</strong></p>
          </div>
        </el-footer>
      </el-container>
    </el-container>

  </div>
</template>

<script setup>
import {Monitor, Compass, Cpu, User} from '@element-plus/icons-vue'

import {computed} from 'vue';
import {useStore} from "vuex";
import {useRouter, useRoute} from "vue-router";

const store = useStore();
const router = useRouter();
const route = useRoute();
const name = computed(() => store.state.name);
const role = localStorage.getItem('role')
const isSuperUser = computed(() => role === '1');
const activeRouter = computed(() => route.name)

const breadcrumbs = computed(() => {
  const matchedRoutes = route.matched;
  return matchedRoutes.map(route => ({
    to: route.path,
    label: route.meta.title || route.name,
  }));
});

function doLogout() {
  store.commit('logout');
  router.push({name: "Login"});
}
</script>

<style scoped>

.el-main {
  box-shadow: inset 14px 0px 15px -24px rgba(0, 36, 100, 0.3);
  background-color: #f2f3f5;
  padding: 0;
}

.el-menu {
  border-right: 0;
}

.el-menu-item {
  border-radius: 10px;
}

.el-menu-item.is-active {
  background-color: aliceblue;
}

.main {
  height: calc(100vh - 72px);
}


.logo-title-container {
  display: flex;
  align-items: center;

}

.pg-header {
  align-items: center;
  height: 72px;
}

.pg-header .top-menu a {
  padding: 0 5px;
  text-decoration: none;
}

.pg-header img {
  height: 100%;
}

.pg-header .logo {
  height: 50px;
  margin-right: 10px;
}

.el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}

.el-dropdown-link:focus-visible {
  outline: unset;
}

.custom-footer {
  text-align: center;
  background-color: #f2f3f5;
}

.footer-text {
  font-size: 12px;
  color: #16191e;
}
</style>