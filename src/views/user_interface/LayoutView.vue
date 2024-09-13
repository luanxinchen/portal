<template>
  <el-container style="height: 100vh;">
    <el-aside width="86px" style="background-color: #545c64">
      <el-scrollbar>
        <div style="margin: 5px 11px;">
          <a href="/portal">
            <div class="logo-container">
              <img src="../../assets/ECUST_logo.png" alt="logo" class="logo-image">
            </div>
          </a>
          <el-menu
              collapse
              background-color="#545c64"
              text-color="#fff"
          >
            <el-menu-item class="custom-menu-item" key="contract" index="contract"
                          @click="handleMenuItemClick(contractItem)">
              <div class="menu-item-container">
                <el-icon>
                  <MapLocation/>
                </el-icon>
                <span class="menu-item-text">职能引导</span>
              </div>
            </el-menu-item>
            <el-menu-item class="custom-menu-item" v-for="item in state.category" :key="item.id" :index="item.id+``"
                          @click="handleMenuItemClick(item)">
              <div class="menu-item-container">
                <el-icon>
                  <component :is="item.icon"/>
                </el-icon>
                <span class="menu-item-text">{{ item.title }}</span>
              </div>
            </el-menu-item>
          </el-menu>
        </div>
      </el-scrollbar>
    </el-aside>
    <el-container>
      <el-header height="72px" style="border-bottom: 1px solid #e5e6eb">
        <el-row class="pg-header" justify="space-between">
          <h3>欢迎访问ECUST计算机学院内网门户</h3>
        </el-row>
      </el-header>
      <el-scrollbar wrap-class="app-main-scroll-wrap">
        <el-main class="body">
          <router-view></router-view>
        </el-main>
        <el-footer class="custom-footer" height="20px">
          <div class="footer-text">
            <p style="margin: 0">© 2024 <strong>ECUST</strong></p>
          </div>
        </el-footer>
        <el-backtop target=".app-main-scroll-wrap">
          <el-icon>
            <ArrowUpBold/>
          </el-icon>
        </el-backtop>
      </el-scrollbar>
    </el-container>
  </el-container>

</template>

<script setup>
import {getCurrentInstance, onMounted, reactive,} from 'vue';
import {ElNotification} from "element-plus";

const {proxy} = getCurrentInstance()
const state = reactive({
  category: [],
  notifications: [],
  notifyPromise: Promise.resolve(),
})

const contractItem = reactive({
  name: 'contract',
  id: '000'
})

const handleMenuItemClick = (item) => {
  if (proxy.$route.path === '/portal') {
    scrollToCategory(item.id);
  } else {
    proxy.$router.push({name: 'Portal'});
  }
}

// 锚定页面
const scrollToCategory = (categoryId) => {
  const targetElement = document.getElementById(categoryId);
  if (targetElement) {
    targetElement.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  }
};

// 获取站点
const initRequest = async () => {
  try {
    const [categoryRes, notifyRes] = await Promise.all([
      proxy.$axios.get('site_category/'),
      proxy.$axios.get('notify/'),
    ])
    state.category = categoryRes.data.results;
    state.notifications = notifyRes.data.results;

    checkAndShowNotifications();
  } catch (error) {
    console.error('Error:', error)
  }
}

const checkAndShowNotifications = () => {
  const currentTime = new Date();
  state.notifications.forEach((notification) => {
    const startTime = new Date(notification.start_time);
    const endTime = new Date(notification.end_time);

    if (notification.is_active && currentTime >= startTime && currentTime <= endTime) {
      state.notifyPromise = state.notifyPromise.then(() => {
        return new Promise((resolve) => {
          ElNotification({
            title: notification.title,
            dangerouslyUseHTMLString: true,
            message: notification.content,
            type: notification.type_text,
            onClose: resolve,
          });
        });
      });
    }
  });
};


onMounted(() => {
  initRequest()
})

</script>

<style scoped>

.body {
  background-color: #f9f9f9;
  padding: 15px 25px;
}

.el-main {
  box-shadow: inset 14px 0px 15px -24px rgba(0, 36, 100, 0.3);
}

.el-menu {
  border-right: 0;
}

.el-menu-item {
  height: 65px;
}

.el-menu-item [class^=el-icon] {
  margin-right: 0;
}

.el-menu-item.is-active .menu-item-container .menu-item-text {
  color: var(--el-menu-active-color);
}

.custom-menu-item {
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 18px;
  border-radius: 10px;
  transition: 0.1s;
}

.menu-item-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.menu-item-text {
  font-size: 12px;
  padding-top: 6px;
  color: #FFF;
}

.logo-container {
  text-align: center;
  margin: 16px 0;
}

.logo-image {
  width: 60px;
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
  height: 35px;
  margin-right: 10px;
}

.el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}

.custom-footer {
  text-align: center;
  background-color: #f9f9f9;
}

.footer-text {
  font-size: 12px;
  color: #16191e;
}

.category-container {
  margin-bottom: 10px;
}

.category-title {
  display: flex;
  align-items: center;
  justify-content: left;
  padding: 10px 10px 15px 0;
}

.site-row {
  margin-left: -10px;
  margin-right: -10px;
}

.card {
  padding: 10px;
}

.card-content {
  border: 1px solid #ebeff5;
  border-radius: 15px;
  background-color: #FFF;
  transition: 0.3s;
  height: 50px;
  display: flex;
  align-items: center;
  padding: 15px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.card-content:hover {
  box-shadow: 0 26px 40px -24px rgba(0, 36, 100, 0.3);
  transform: translateY(-3px);
}

.card-image {
  max-width: 40px;
  max-height: 40px;
  width: 100%;
  height: auto;
  flex-shrink: 0;
  margin-right: 15px;
}

.card-text {
  flex-grow: 1;
}

.card-title {
  font-size: 0.8em;
  color: #454545;
  margin-top: 5px;
  margin-bottom: 5px;
}

.card-text p {
  color: #979898;
  font-size: 12px;
  margin-top: 1px;
}

.hover-icon {
  position: absolute;
  top: 10px;
  right: 10px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.card-content:hover .hover-icon {
  opacity: 1;
}

.el-backtop {
  border-radius: 8px;
  font-size: 16px;
  border: 1px solid #ebeff5;
  --el-backtop-text-color: #545c64;
  transition: 0.2s;
  box-shadow: none;
}

.el-backtop:hover {
  --el-backtop-text-color: var(--el-color-primary);
}

</style>