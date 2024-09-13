<template>
  <!-- 列表-->
  <el-card class="box-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>职能列表</span>
      </div>
      <el-row :gutter="20" style="margin-top: 10px">
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
        <el-col :span="6" class="flex-container" :offset="12">
          <el-col class="select-container">
            <el-input clearable :prefix-icon="Search" v-model="searchForm.search" placeholder="请输入关键字"
                      @blur="handleSearch"/>
          </el-col>
        </el-col>
      </el-row>
    </template>

    <el-row :gutter="20" style="margin-bottom: 10px">
      <el-col :span="16">
        <el-button type="primary" :icon="Plus" @click="handleAdd" auto-insert-space>添加</el-button>
        <el-button type="primary" plain :icon="View" @click="handleReview" auto-insert-space>预览</el-button>
      </el-col>
    </el-row>
    <el-table :data="state.contact" width="100%" @sort-change="handleSortChange">
      <el-table-column prop="sort" label="排序" sortable="custom" width="80"/>
      <el-table-column prop="description" label="职能描述" show-overflow-tooltip/>
      <el-table-column prop="category_cn" label="分类" sortable="custom" width="100">
        <template #default="{ row }">
          <span v-html="row.category_cn"></span>
        </template>
      </el-table-column>
      <el-table-column prop="person" label="联系人" show-overflow-tooltip sortable="custom" width="100"/>
      <el-table-column prop="location" label="位置" show-overflow-tooltip/>
      <el-table-column prop="contact_type_cn" label="联系类型" width="100">
        <template #default="{row}">
          {{ row.contact_type_cn }}
        </template>
      </el-table-column>
      <el-table-column prop="contact_key" label="联系方式" show-overflow-tooltip/>
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
      title="职能信息"
      align-center
      :close-on-click-modal="true"
      destroy-on-close
  >
    <el-form
        :model="currentItem"
        :rules="formRule"
        ref="submitRef"
        label-width="auto">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="职责描述" prop="description">
            <el-input v-model="currentItem.description"/>
          </el-form-item>
          <el-form-item label="位置" prop="location">
            <el-input v-model="currentItem.location"/>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="联系人" prop="person">
            <el-input v-model="currentItem.person"/>
          </el-form-item>
          <el-form-item label="联系方式" prop="contact_key">
            <el-input v-model="currentItem.contact_key"/>
          </el-form-item>

        </el-col>
      </el-row>
      <el-form-item label="联系类型" prop="contact_type">
        <el-radio-group v-model="currentItem.contact_type">
          <el-radio label="0">无</el-radio>
          <el-radio label="1">手机号码</el-radio>
          <el-radio label="2">企业微信</el-radio>
          <el-radio label="3">企业邮箱</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="分类" prop="category">
            <el-select v-model="currentItem.category" placeholder="请选择分类">
              <el-option v-for="category in state.category" :key="category.id" :label="category.title"
                         :value="category.id"/>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="排序" prop="sort">
            <el-input-number v-model="currentItem.sort"/>
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
  contact: [],
  category: [],
})

const dialogVisible = ref(false);
const total = ref(0)        // 总数据量
const pageSize = ref(10)    // 每页数据量
const currentPage = ref(1)  // 当前页码
const searchForm = reactive({
  search: "",
  category_id: null,
});
const currentItem = reactive({
  id: null,
  category_cn: "",
  person: "",
  location: "",
  description: "",
  sort: 0,
  contact_type: "",
  category: 0,
  contact_key: "",
});
const formRule = reactive({
  person: [
    {required: true, message: '请输入联系人', trigger: 'blur'},
  ],
  category: [
    {required: true, message: '请选择分类', trigger: 'blur'},
  ],
  location: [
    {required: true, message: '请输入位置', trigger: 'blur'},
  ],
  sort: [
    {required: true, message: '请输入排序号', trigger: 'blur'},
  ],
  description: [
    {required: true, message: '请输入职责描述', trigger: 'blur'},
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
      proxy.$axios.get(`contact/`, {params: search_param}),
      proxy.$axios.get('contact_category/'),
    ])
    state.contact = sitesRes.data.results
    total.value = sitesRes.data.count
    state.category = categoryRes.data.results
  } catch (error) {
    console.error('Error:', error)
  }
}

const handleAdd = () => {
  Object.assign(currentItem, {
    id: null,
    category_cn: "",
    person: "",
    location: "",
    description: "",
    sort: 1,
    contact_type: "",
    category: "",
    contact_key: "",
  })
  dialogVisible.value = true
}

const handleEdit = (index, row) => {
  Object.assign(currentItem, {
    id: row.id,
    category_cn: row.category_cn,
    person: row.person,
    location: row.location,
    description: row.description,
    sort: row.sort,
    contact_type: row.contact_type.toString(),
    category: row.category,
    contact_key: row.contact_key,
  })
  dialogVisible.value = true
}

const handleDelete = (index, row) => {
  proxy.$axios
      .delete(`contact/${row.id}/`)
      .then(() => {
        state.contact.splice(index, 1)
        dialogVisible.value = false
        ElMessage.success('删除成功')
      })
      .catch((error) => {
        console.error('Error:', error)
      })
}

function handleSubmit() {
  proxy.$refs.submitRef.validate((valid) => {
    if (valid) {
      // 构造提交表单
      const formData = new FormData();
      formData.append('person', currentItem.person);
      formData.append('location', currentItem.location);
      formData.append('description', currentItem.description);
      formData.append('sort', currentItem.sort);
      formData.append('category', currentItem.category);
      formData.append('contact_type', currentItem.contact_type);
      formData.append('contact_key', currentItem.contact_key);

      if (currentItem.id === null) {
        // 添加数据
        proxy.$axios.post("contact/", formData).then((res) => {
          state.contact.push(res.data);
          dialogVisible.value = false;
          ElMessage.success("添加成功")
        });
      } else {
        // 更新数据
        proxy.$axios.patch(`contact/${currentItem.id}/`, formData).then((res) => {
          const index = state.contact.findIndex((site) => site.id === currentItem.id);
          state.contact.splice(index, 1, res.data);
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

.avatar-uploader .avatar {
  width: 150px;
  height: 150px;
  display: block;
}

.avatar-uploader {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
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