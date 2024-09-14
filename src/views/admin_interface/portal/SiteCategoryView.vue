<template>
  <!-- 列表-->
  <el-card class="box-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>站点分类列表</span>
        <el-button type="primary" :icon="Plus" plain @click="handleAdd">添加</el-button>
      </div>
    </template>

    <el-table :data="state.category" width="100%" @sort-change="handleSortChange" style="height: calc(100vh - 290px);">
      <el-table-column prop="id" label="ID" sortable/>
      <el-table-column prop="sort" label="排序" sortable/>
      <el-table-column prop="title" label="标题" sortable/>
      <el-table-column prop="icon" label="图标">
        <template v-slot="{ row }">
          <el-icon>
            <component :is="row.icon"/>
          </el-icon>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" min-width="160"/>
      <el-table-column prop="updated_at" label="更新时间" min-width="160"/>
      <el-table-column fixed="right" width="150">
        <template #header>
          <el-input :prefix-icon="Search" v-model="searchForm.search" placeholder="请输入关键字"
                    size="small" @blur="handleSearch"/>
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
      title="站点分类信息"
      align-center
      :close-on-click-modal="true"
  >
    <el-form
        :model="currentItem"
        :rules="formRule"
        ref="submitRef">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="标题" prop="title">
            <el-input v-model="currentItem.title"/>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="图标" prop="icon">
            <el-input v-model="currentItem.icon" placeholder="请输入Icon名称"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item label="排序" prop="sort">
        <el-input-number v-model="currentItem.sort"/>
      </el-form-item>
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
import {Plus, InfoFilled, Search} from '@element-plus/icons-vue'
import {ElMessage} from 'element-plus'

const {proxy} = getCurrentInstance()

const state = reactive({
  category: [],
})

const dialogVisible = ref(false);
const total = ref(0)        // 总数据量
const pageSize = ref(10)    // 每页数据量
const currentPage = ref(1)  // 当前页码
const searchForm = reactive({
  search: "",
});
const currentItem = reactive({
  id: null,
  title: "",
  icon: "",
  sort: 0,
});
const formRule = reactive({
  title: [
    {required: true, message: '请输入标题', trigger: 'blur'},
  ],
  icon: [
    {required: true, message: '请输入icon名称', trigger: 'blur'},
  ],
  sort: [
    {required: true, message: '请输入排序号', trigger: 'blur'},
  ]
})

function handleSizeChange(size) {
  pageSize.value = size;
  currentPage.value = 1;
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

const initRequest = async () => {
  let search_param = {
    page: currentPage.value,
    limit: pageSize.value
  }

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
    const [categoryRes] = await Promise.all([
      proxy.$axios.get('site_category/', {params: search_param}),
    ])
    state.category = categoryRes.data.results
    total.value = categoryRes.data.count
  } catch (error) {
    console.error('Error:', error)
  }
}


const handleAdd = () => {
  Object.assign(currentItem, {
    id: null,
    title: '',
    icon: '',
    sort: 1,
  })
  dialogVisible.value = true
}

const handleEdit = (index, row) => {
  Object.assign(currentItem, {
    id: row.id,
    title: row.title,
    icon: row.icon,
    sort: row.sort,
  })
  dialogVisible.value = true
}

const handleDelete = (index, row) => {
  proxy.$axios
      .delete(`site_category/${row.id}/`)
      .then(() => {
        state.category.splice(index, 1)
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
      formData.append('title', currentItem.title);
      formData.append('sort', currentItem.sort);
      formData.append('icon', currentItem.icon);

      if (currentItem.id === null) {
        // 添加数据
        proxy.$axios.post("site_category/", formData).then((res) => {
          state.category.push(res.data);
          dialogVisible.value = false;
          ElMessage.success("添加成功")
        });
      } else {
        // 更新数据
        proxy.$axios.patch(`site_category/${currentItem.id}/`, formData).then((res) => {
          const index = state.category.findIndex((category) => category.id === currentItem.id);
          state.category.splice(index, 1, res.data);
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
</style>