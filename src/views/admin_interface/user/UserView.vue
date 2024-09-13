<template>
  <!-- 列表-->
  <el-card class="box-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>用户列表</span>
        <el-button type="primary" :icon="Plus" plain @click="handleAdd">添加</el-button>
      </div>
    </template>
    <el-table
        :stripe="true"
        :data="state.users"
        width="100%"
        @sort-change="handleSortChange"
        style="height: calc(100vh - 290px);"
    >
      <el-table-column prop="id" label="ID" sortable="custom"/>
      <el-table-column prop="username" label="用户名" sortable/>
      <el-table-column prop="email" label="邮箱" show-overflow-tooltip sortable/>
      <el-table-column prop="role" label="用户角色" sortable>
        <template #default="{ row }">
          <el-tag effect="dark" :type="row.role === 1 ? 'success' : 'primary'">
            {{ row.role === 1 ? '超级管理员' : '网站管理员' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="账号状态" sortable>
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'success' : 'danger'">
            {{ row.status === 1 ? '激活' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" show-overflow-tooltip/>
      <el-table-column prop="updated_at" label="更新时间" show-overflow-tooltip/>
      <el-table-column fixed="right" width="240">
        <template #header>
          <el-input :prefix-icon="Search" v-model="searchForm.search" placeholder="请输入关键字"
                    size="small" @blur="handleSearch" clearable/>
        </template>
        <template #default="scope">
          <el-button size="small" type="primary" plain @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
          <el-button size="small" type="primary" plain @click="handleReset(scope.$index, scope.row)">重置密码
          </el-button>
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

  <el-dialog
      v-model="dialogVisible"
      title="用户信息"
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
          <el-form-item label="用户名" prop="username">
            <el-input v-model="currentItem.username"/>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="currentItem.email"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row v-if="!isEditMode" :gutter="20">
        <el-col :span="12">
          <el-form-item label="密码" prop="password">
            <el-input show-password v-model="currentItem.password"/>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="确认密码" prop="confirm_password">
            <el-input show-password v-model="currentItem.confirm_password"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="用户角色" prop="role">
            <el-radio-group v-model="currentItem.role">
              <el-radio border :label="1">超级管理员</el-radio>
              <el-radio border :label="2">网站管理员</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="状态" prop="status">
            <el-radio-group v-model="currentItem.status">
              <el-radio-button :label="1">激活</el-radio-button>
              <el-radio-button :label="2">禁用</el-radio-button>
            </el-radio-group>
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
  <el-dialog
      v-model="resetDialogVisible"
      :title="`${currentItem.username} - 重置密码`"
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
          <el-form-item label="密码" prop="password">
            <el-input show-password v-model="currentItem.password"/>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="确认密码" prop="confirm_password">
            <el-input show-password v-model="currentItem.confirm_password"/>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="resetDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleResetSubmit">提交</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import {ref, reactive, onMounted, getCurrentInstance,} from 'vue'
import {Search, Refresh, InfoFilled, Plus} from '@element-plus/icons-vue'
import {ElMessage} from "element-plus";

const {proxy} = getCurrentInstance()

const state = reactive({
  users: [],
})
const isEditMode = ref(false);
const dialogVisible = ref(false);
const resetDialogVisible = ref(false);
const total = ref(0)        // 总数据量
const pageSize = ref(10)    // 每页数据量
const currentPage = ref(1)  // 当前页码
const searchForm = reactive({
  search: "",
  employee_status: null,
  is_active: null
});

const currentItem = reactive({
  id: null,
  username: "",
  email: "",
  password: "",
  confirm_password: "",
  role: 1,
  status: 1,
});

const validateEmail = (rule, value, callback) => {
  const emailRegex = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
  if (!emailRegex.test(value)) {
    callback(new Error('请输入有效的邮箱地址'));
  } else {
    callback();
  }
};

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== currentItem.password) {
    callback(new Error('两次输入的密码不一致'));
  } else {
    callback();
  }
};

const formRule = reactive({
  username: [
    {required: true, message: '请输入用户名', trigger: 'blur'},
  ],
  email: [
    {required: true, message: '请输入邮箱', trigger: 'blur'},
    {validator: validateEmail, trigger: 'blur'},
  ],
  password: [
    {required: true, message: '请输入密码', trigger: 'blur'},
  ],
  confirm_password: [
    {required: true, message: '请确认密码', trigger: 'blur'},
    {validator: validateConfirmPassword, trigger: 'blur'},
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

const handleAdd = () => {
  isEditMode.value = false;
  Object.assign(currentItem, {
    id: null,
    username: "",
    email: "",
    password: "",
    confirm_password: "",
    role: 1,
    status: 1,
  })
  dialogVisible.value = true
}

const handleEdit = (index, row) => {
  isEditMode.value = true;
  Object.assign(currentItem, {
    id: row.id,
    username: row.username,
    email: row.email,
    password: row.password,
    confirm_password: row.password,
    role: row.role,
    status: row.status,
  })
  dialogVisible.value = true
}

const handleReset = (index, row) => {
  Object.assign(currentItem, {
    id: row.id,
    username: row.username,
    password: row.password,
    confirm_password: row.password,
  })
  resetDialogVisible.value = true
}

function handleSubmit() {
  proxy.$refs.submitRef.validate((valid) => {
    if (valid) {
      // 构造提交表单
      const formData = new FormData();
      formData.append('username', currentItem.username);
      formData.append('email', currentItem.email);
      formData.append('password', currentItem.confirm_password);
      formData.append('role', currentItem.role);
      formData.append('status', currentItem.status);

      if (currentItem.id === null) {
        // 添加数据
        proxy.$axios.post("users/", formData).then((res) => {
          state.users.push(res.data);
          dialogVisible.value = false;
          ElMessage.success("添加成功")
        });
      } else {
        // 更新数据
        proxy.$axios.patch(`users/${currentItem.id}/`, formData).then((res) => {
          const index = state.users.findIndex((site) => site.id === currentItem.id);
          state.users.splice(index, 1, res.data);
          dialogVisible.value = false;
          ElMessage.success("更新成功")
        });
      }
    } else {
      return false;
    }
  })

}

function handleResetSubmit() {
  proxy.$refs.submitRef.validate((valid) => {
    if (valid) {
      // 构造提交表单
      const formData = new FormData();
      formData.append('password', currentItem.confirm_password);
      proxy.$axios.patch(`users/${currentItem.id}/`, formData).then((res) => {
        const index = state.users.findIndex((site) => site.id === currentItem.id);
        state.users.splice(index, 1, res.data);
        resetDialogVisible.value = false;
        ElMessage.success("密码更新成功")
      });
    }
  })
}

const handleDelete = (index, row) => {
  proxy.$axios
      .delete(`users/${row.id}/`)
      .then(() => {
        state.users.splice(index, 1)
        dialogVisible.value = false
        ElMessage.success('删除成功')
      })
      .catch((error) => {
        console.error('Error:', error)
      })
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
    const [UserRes] = await Promise.all([
      proxy.$axios.get(`users/`, {params: search_param})
    ])
    state.users = UserRes.data.results
    total.value = UserRes.data.count
  } catch (error) {
    console.error('Error:', error)
  }
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