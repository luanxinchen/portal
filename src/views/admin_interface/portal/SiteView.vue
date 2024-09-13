<template>
  <!-- 列表-->
  <el-card class="box-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>站点列表</span>
      </div>
      <el-row :gutter="20" style="margin-top: 10px">
        <el-col :span="6" class="flex-container">
          <el-col :span="6" class="label-container">
            <p>状态</p>
          </el-col>
          <el-col :span="18" class="select-container">
            <el-select
                v-model="searchForm.is_active"
                clearable
                placeholder="请选择"
                @change="handleSearch"
            >
              <el-option label="是" value="1">启用</el-option>
              <el-option label="否" value="0">禁用</el-option>
            </el-select>
          </el-col>
        </el-col>
        <el-col :span="6" class="flex-container">
          <el-col :span="6" class="label-container">
            <p>分类</p>
          </el-col>
          <el-col :span="18" class="select-container">
            <el-select
                v-model="searchForm.category_id"
                clearable
                placeholder="请选择"
                @change="handleSearch"
            >
              <el-option
                  v-for="item in state.category"
                  :key="item.id"
                  :label="item.title"
                  :value="item.id"
              />
            </el-select>
          </el-col>
        </el-col>
        <el-col :span="6" class="flex-container">
          <el-col class="select-container">
            <el-input :prefix-icon="Search" v-model="searchForm.search" placeholder="请输入关键字"
                      @blur="handleSearch"/>
          </el-col>
        </el-col>
        <el-col :span="6" class="flex-container">
          <el-button type="primary" :icon="Search" @click="handleSearch" auto-insert-space>搜索</el-button>
          <el-button type="info" text bg :icon="Refresh" @click="handleSearchReset" auto-insert-space>重置</el-button>
        </el-col>
      </el-row>
    </template>

    <el-row :gutter="20" style="margin-bottom: 10px">
      <el-col :span="24">
        <el-button type="primary" :icon="Plus" @click="handleAdd" auto-insert-space>添加</el-button>
        <el-button type="primary" plain :icon="View" @click="handleReview" auto-insert-space>预览</el-button>
      </el-col>
    </el-row>
    <el-table :data="state.sites" width="100%" @sort-change="handleSortChange" style="height: calc(100vh - 377px);">
      <el-table-column prop="logo" label="Logo" width="60">
        <template #default="{ row }">
          <div style="display: flex; align-items: center;justify-content: center">
            <el-image :src="row.logo" alt="Logo" style="min-width:30px;height:30px"/>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="sort" label="排序" sortable="custom"/>
      <el-table-column prop="title" label="标题" sortable="custom" show-overflow-tooltip/>
      <el-table-column prop="category_cn" label="分类" sortable="custom"/>
      <el-table-column prop="maintainer_cn" label="管理员"/>
      <el-table-column prop="description" label="子标题" show-overflow-tooltip/>
      <el-table-column prop="tips" label="网站提示" show-overflow-tooltip/>
      <el-table-column prop="is_active" label="状态" sortable="custom">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'">
            {{ row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="url" label="链接" show-overflow-tooltip/>

      <el-table-column fixed="right" width="150">
        <template #header>
          操作
        </template>
        <template #default="scope">
          <el-button size="small" type="primary" plain @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
          <el-popconfirm
              confirm-button-text="是"
              cancel-button-text="否"
              :icon="InfoFilled"
              icon-color="#626AEF"
              title="确定删除吗?"
              :hide-after="0"
              @confirm="handleDelete(scope.$index, scope.row)"
          >
            <template #reference>
              <el-button size="small" type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <div class="example-pagination-block">
      <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10,20, 50, 100]"
          :small="true"
          :background="true"
          layout="->,total,sizes,prev, pager, next,jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
      />
    </div>
  </el-card>
  <!-- 编辑/添加表单 -->
  <el-dialog
      v-model="dialogVisible"
      title="站点信息"
      :close-on-click-modal="true"
      width="70%"
  >
    <el-form
        :model="currentItem"
        :rules="formRule"
        ref="submitRef"
        label-width="auto"
        enctype="multipart/form-data">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="标题" prop="title">
            <el-input v-model="currentItem.title"/>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="描述" prop="description">
            <el-input v-model="currentItem.description"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="链接" prop="url">
            <el-input v-model="currentItem.url"/>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="管理员" prop="maintainer">
            <el-select
                v-model="currentItem.maintainer"
                filterable
                remote
                reserve-keyword
                placeholder="搜索用户"
                :remote-method="remoteMethod"
                :loading="loading"
                style="width: 240px"
                clearable
            >
              <el-option
                  v-for="user in users"
                  :key="user.label"
                  :label="user.label"
                  :value="user.value"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="提示" prop="tips">
            <el-input v-model="currentItem.tips"/>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="分类" prop="category">
            <el-select v-model="currentItem.category" placeholder="请选择分类">
              <el-option v-for="category in state.category" :key="category.id" :label="category.title"
                         :value="category.id"/>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="排序" prop="sort">
            <el-input-number v-model="currentItem.sort"/>
          </el-form-item>
          <el-form-item label="状态" prop="is_active">
            <el-radio-group v-model="currentItem.is_active">
              <el-radio-button label="启用" :value="true" />
              <el-radio-button label="禁用" :value="false" />
            </el-radio-group>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="Logo">
            <el-upload
                action=""
                class="avatar-uploader"
                :show-file-list="false"
                :before-upload="handleBeforeUpload"
            >
              <img v-if="currentItem.logo" :src="currentItem.logo" class="avatar"/>
              <el-icon v-else class="avatar-uploader-icon">
                <plus/>
              </el-icon>
            </el-upload>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">提交</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import {ref, reactive, onMounted, getCurrentInstance,} from 'vue'
import {Plus, InfoFilled, Search, Download, Refresh, View} from '@element-plus/icons-vue'
import {ElMessage} from 'element-plus'

const {proxy} = getCurrentInstance()

const state = reactive({
  sites: [],
  category: [],
})
const users = ref([]);
const loading = ref(false)
const dialogVisible = ref(false);
const total = ref(0)        // 总数据量
const pageSize = ref(10)    // 每页数据量
const currentPage = ref(1)  // 当前页码
const searchForm = reactive({
  search: "",
  category_id: null,
  is_active: null,
  maintainer: "",
  tips: ""
});
const currentItem = reactive({
  id: null,
  category_cn: "",
  title: "",
  url: "",
  description: "",
  sort: 0,
  logo: null,
  category: 0,
  is_active: "",
  maintainer: "",
  tips: ""
});
const formRule = reactive({
  title: [
    {required: true, message: '请输入标题', trigger: 'blur'},
  ],
  category: [
    {required: true, message: '请选择分类', trigger: 'blur'},
  ],
  url: [
    {required: true, message: '请输入链接', trigger: 'blur'},
    {type: 'url', message: "请输入正确的url", trigger: 'change'}
  ],
  sort: [
    {required: true, message: '请输入排序号', trigger: 'blur'},
  ],
  description: [
    {required: true, message: '请添加网站描述', trigger: 'blur'},
  ],
  maintainer: [
    {required: true, message: '请输入网站管理员', trigger: 'blur'},
  ],
})

function handleSizeChange(size) {
  pageSize.value = size;
  currentPage.value = 1;  // 重置当前页码为1
  initRequest();
}

// 切换页码时刷新页码并重载数据
function handlePageChange(current) {
  currentPage.value = current;
  initRequest()
}

function handleSearch() {
  currentPage.value = 1;
  initRequest();
}

function handleSearchReset() {
  searchForm.search = "";
  searchForm.category_id = null;
  searchForm.is_active = null;
  initRequest();
}

function handleReview() {
  window.open('/portal', '_blank')
}

const sortData = ref({
  prop: '',  // 排序字段
  order: ''
});

function handleSortChange(data) {
  // 处理后端级联排序
  if (data.prop.endsWith('_cn')) {
    data.prop = data.prop.slice(0, -3);
  }
  sortData.value = data;
  initRequest();
}

const remoteMethod = async (query) => {
  if (query !== '') {
    loading.value = true;
    try {
      const response = await proxy.$axios.get(`users/`, {params: {search: query}});
      users.value = response.data.results.map(user => ({
        value: user.id,
        label: user.username,
      }));
    } catch (error) {
      console.error('Error:', error);
    } finally {
      loading.value = false;
    }
  } else {
    users.value = [];
  }
};

const initRequest = async () => {
  let search_param = {
    page: currentPage.value,
    limit: pageSize.value,
  }

  // 处理排序方式
  if (sortData.value.order) {
    search_param.ordering = sortData.value.order === 'ascending'
        ? sortData.value.prop
        : `-${sortData.value.prop}`;
  }

  for (let key in searchForm) {
    let value = searchForm[key];
    if (!value) {
      continue
    }
    search_param[key] = value;
  }

  try {
    const [sitesRes, categoryRes] = await Promise.all([
      proxy.$axios.get(`site/`, {params: search_param}),
      proxy.$axios.get('site_category/'),
    ])
    state.sites = sitesRes.data.results
    total.value = sitesRes.data.count
    state.category = categoryRes.data.results
  } catch (error) {
    console.error('Error:', error)
  }
}


const handleAdd = () => {
  Object.assign(currentItem, {
    id: null,
    category_cn: '',
    title: '',
    url: '',
    description: '',
    sort: 1,
    logo: null,
    category: null,
    logoFile: null,
    is_active: true,
    maintainer: '',
    tips: ''
  })
  dialogVisible.value = true
}

const handleEdit = (index, row) => {
  Object.assign(currentItem, {
    id: row.id,
    category_cn: row.category_cn,
    title: row.title,
    url: row.url,
    description: row.description,
    sort: row.sort,
    logo: row.logo,
    category: row.category,
    is_active: row.is_active,
    logoFile: null,
    maintainer: row.maintainer,
    tips: row.tips
  })
  dialogVisible.value = true
}

const handleDelete = (index, row) => {
  proxy.$axios
      .delete(`site/${row.id}/`)
      .then(() => {
        state.sites.splice(index, 1)
        dialogVisible.value = false
        ElMessage.success('删除成功')
      })
      .catch((error) => {
        console.error('Error:', error)
      })
}


function handleBeforeUpload(file) {
  // 构造图片本地链接
  var windowURL = window.URL || window.webkitURL;
  currentItem.logo = windowURL.createObjectURL(file);
  // 创建文件对象
  currentItem.logoFile = file
  return false;
}

function handleSubmit() {
  proxy.$refs.submitRef.validate((valid) => {
    if (valid) {
      // 构造提交表单
      const formData = new FormData();
      formData.append('title', currentItem.title);
      formData.append('url', currentItem.url);
      formData.append('description', currentItem.description);
      formData.append('sort', currentItem.sort);
      formData.append('category', currentItem.category);
      formData.append('is_active', currentItem.is_active);
      formData.append('maintainer', currentItem.maintainer);
      formData.append('tips', currentItem.tips);
      // 非必填项
      if (currentItem.logoFile) {
        formData.append('logo', currentItem.logoFile);
      }


      if (currentItem.id === null) {
        // 添加数据
        proxy.$axios.post("site/", formData).then((res) => {
          state.sites.push(res.data);
          dialogVisible.value = false;
          ElMessage.success("添加成功")
        });
      } else {
        // 更新数据
        proxy.$axios.patch(`site/${currentItem.id}/`, formData).then((res) => {
          const index = state.sites.findIndex((site) => site.id === currentItem.id);
          state.sites.splice(index, 1, res.data);
          dialogVisible.value = false;
          ElMessage.success("更新成功")
        });
      }
    } else {
      return false;
    }
  })

}

onMounted(() => {
  initRequest()
})
</script>

<style scoped>

.box-card {
  margin: 0 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-footer button:first-child {
  margin-right: 10px;
}

.example-pagination-block {
  margin-top: 10px;
}

.example-pagination-block .example-demonstration {
  margin-bottom: 16px;
}

.avatar-uploader {
  width: 100px;
  height: 100px;
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .avatar {
  width: 100px;
  height: 100px;
  display: block;
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  text-align: center;
}

.flex-container {
  display: flex;
  justify-content: right;
  align-items: center;
}

.label-container {
  font-size: 14px;
}

.select-container {
  flex: 1;
}
</style>