<template>
  <div class="category-container" id="000">
    <a class="category-title">职能引导</a>
    <div style="background-color: #FFFFFF;border: 1px solid #ebeff5;border-radius: 15px;padding: 0px 15px 10px 15px">
      <el-tabs v-model="activeTab">
        <el-tab-pane v-for="category in state.contact_category" :key="category.id"
                     :name="category.title">
          <template #label>
            <span v-html="category.title"></span>
          </template>
          <el-table :data="category.contacts" size="small" height="159" style="width: 100%;">
            <el-table-column prop="description" label="职能描述" show-overflow-tooltip/>
            <el-table-column prop="person" label="联系人" show-overflow-tooltip/>
            <el-table-column prop="location" label="位置" show-overflow-tooltip/>
            <el-table-column prop="contact_key" label="联系方式" show-overflow-tooltip/>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
  <div v-for="item in state.category" :key="item.id" class="category-container" :id="item.id">
    <a class="category-title">{{ item.title }}</a>
    <el-row :gutter="28" class="site-row">
      <el-col :xs="24" :sm="12" :md="8" :lg="6" :xl="4" v-for="site in item.sites" :key="site.id" class="card">
        <div class="card-content" @click="openSite(site.url)">
          <img :src="site.logo" :alt="site.title" class="card-image">
          <div class="card-text">
            <h5 class="card-title">{{ site.title }}</h5>
            <p>{{ site.description }}</p>
          </div>
          <div class="hover-icon">
            <el-popover
                :width="250"
                popper-style="box-shadow: rgba(0, 36, 100, 0.3) 0px 10px 38px -10px, rgba(0, 36, 100, 0.3) 0px 10px 20px -15px; padding: 20px;border-radius:10px"
                :show-after="50"
                :hide-after="50"
            >
              <template #reference>
                <el-icon color="#454545">
                  <InfoFilled/>
                </el-icon>
              </template>
              <template #default>
                <div style="display: flex; gap: 16px; flex-direction: column">
                  <el-avatar
                      :size="40"
                      :src="site.logo"
                      style="background-color:#FFFFFF;"
                      shape="square"
                  />
                  <div>

                    <p style="margin-bottom: 5px;">
                      {{ site.description }}
                    </p>
                    <p style="margin: 0; font-size: 14px; color: var(--el-color-info)">
                      @{{ site.maintainer_cn }}
                    </p>
                  </div>
                  <p style="margin: 0;font-size: 12px">
                    <el-icon>
                      <Flag/>
                    </el-icon>
                    {{ site.tips }}
                  </p>
                  <p style="margin: 0;font-size: 12px">
                    {{ site.url }}
                  </p>
                </div>
              </template>
            </el-popover>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import {getCurrentInstance, onMounted, reactive,} from 'vue';

let activeTab = 0

const {proxy} = getCurrentInstance()
const state = reactive({
  category: [],
  contact_category: []
})

function openSite(url) {
  window.open(url, '_blank')
}

// 获取站点
const initRequest = async () => {
  try {
    const [categoryRes, contact_categoryRes] = await Promise.all([
      proxy.$axios.get('site_category/'),
      proxy.$axios.get('contact_category/'),
    ])
    state.category = categoryRes.data.results;
    state.contact_category = contact_categoryRes.data.results;

    if (state.contact_category.length > 0) {
      activeTab = state.contact_category[0].title;  // 默认激活第一个tab
    }
  } catch (error) {
    console.error('Error:', error)
  }
}

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
  width: 40px;
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
  padding: 15px;
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

:deep(.el-tabs__header) {
  margin: 0 0 5px;
}

</style>