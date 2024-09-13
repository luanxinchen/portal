<template>
  <!-- 列表-->
  <el-card class="box-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>通知发布列表</span>
        <el-button type="primary" :icon="Plus" plain @click="handleAdd">添加</el-button>
      </div>
    </template>

    <el-table :data="state.notify" width="100%" @sort-change="handleSortChange">
      <el-table-column prop="id" label="ID" width="80" sortable="custom"/>
      <el-table-column prop="title" label="通知标题" sortable="custom"/>
      <el-table-column prop="content" label="通知内容" sortable="custom">
        <template #default="{row}">
          <el-tooltip
              :content=row.content
              placement="top"
          >
            <el-link type="primary">预览<el-icon class="el-icon--right"><View/></el-icon></el-link>

          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column prop="start_time" label="开始时间" show-overflow-tooltip sortable="custom"/>
      <el-table-column prop="end_time" label="结束时间" show-overflow-tooltip sortable="custom"/>
      <el-table-column prop="type_text" label="通知类别">
        <template #default="{row}">
          <el-tag :type="row.type_text">{{ row.type_text }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_active" label="状态" sortable="custom">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'">
            {{ row.is_active ? '激活' : '失效' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column fixed="right"  width="200">
        <template #header>
          <el-input :prefix-icon="Search" size="small" v-model="searchForm.search" placeholder="请输入关键字"
                    @blur="handleSearch"/>
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
          v-model="currentPage"
          :total="total"
          :page-size="pageSize"
          :small="true"
          :background="true"
          layout="->,prev, pager, next,total,jumper"
          @current-change="handlePageChange"
      />
    </div>
  </el-card>
  <!-- 编辑/添加表单 -->
  <el-drawer
      v-model="dialogVisible"
      title="通知发布信息"
      direction="rtl"
      :close-on-click-modal="true"
      :size="'35%'"
  >
    <el-form
        :model="currentItem"
        :rules="formRule"
        ref="submitRef"
        :label-position="'top'"
        enctype="multipart/form-data">
      <el-form-item label="通知标题" prop="title">
        <el-input v-model="currentItem.title"/>
      </el-form-item>
      <el-form-item label="通知内容 (支持html) " prop="content">
        <el-input v-model="currentItem.content" type="textarea"/>
      </el-form-item>
      <el-form-item label="时间范围" prop="end_time">
        <el-date-picker
            v-model="datetimeRange"
            type="datetimerange"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
            @change="handleTimeChange"
        />
      </el-form-item>
      <el-form-item label="通知类型" prop="type">
        <el-radio-group v-model="currentItem.type">
          <el-radio label="0">Info</el-radio>
          <el-radio label="1">Success</el-radio>
          <el-radio label="2">Warning</el-radio>
          <el-radio label="3">Error</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="状态" prop="is_active">
        <el-switch
            v-model="currentItem.is_active"
            inline-prompt/>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">提交</el-button>
      </span>
    </template>
  </el-drawer>
</template>

<script setup>
import {ref, reactive, onMounted, getCurrentInstance,} from 'vue'
import {Plus, InfoFilled, Search} from '@element-plus/icons-vue'
import {ElMessage} from 'element-plus'

const {proxy} = getCurrentInstance()

const state = reactive({
  notify: [],
})

const dialogVisible = ref(false);
const total = ref(0)        // 总数据量
const pageSize = ref(10)    // 每页数据量
const currentPage = ref(1)  // 当前页码
const searchForm = reactive({
  search: "",
});
const datetimeRange = ref([])

const currentItem = reactive({
  id: null,
  title: "",
  content: "",
  start_time: "",
  end_time: "",
  is_active: 1,
  type: "",
});

const handleTimeChange = (value) => {
  currentItem.start_time = value[0];
  currentItem.end_time = value[1];
};

const formRule = reactive({
  title: [
    {required: true, message: '请输入标题', trigger: 'blur'},
  ],
  content: [
    {required: true, message: '请输入内容', trigger: 'blur'},
  ],
  end_time: [
    {required: true, message: '请选择时间范围', trigger: 'blur'},
  ]
})

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
  if (data.prop.endsWith('_text')) {
    data.prop = data.prop.slice(0, -5);
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
    const [notifyRes] = await Promise.all([
      proxy.$axios.get('notify/', {params: search_param}),
    ])
    state.notify = notifyRes.data.results
    total.value = notifyRes.data.count
  } catch (error) {
    console.error('Error:', error)
  }
}


const handleAdd = () => {
  datetimeRange.value = []
  Object.assign(currentItem, {
    id: null,
    title: '',
    content: '',
    start_time: '',
    end_time: '',
    is_active: true,
    type: '0',
  })
  dialogVisible.value = true
}

const handleEdit = (index, row) => {
  Object.assign(currentItem, {
    id: row.id,
    title: row.title,
    content: row.content,
    start_time: row.start_time,
    end_time: row.end_time,
    is_active: row.is_active,
    type: row.type.toString(),
  });
  datetimeRange.value = [row.start_time, row.end_time];

  dialogVisible.value = true
}

const handleDelete = (index, row) => {
  proxy.$axios
      .delete(`notify/${row.id}/`)
      .then(() => {
        state.notify.splice(index, 1)
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
      formData.append('content', currentItem.content);
      formData.append('start_time', currentItem.start_time);
      formData.append('end_time', currentItem.end_time);
      formData.append('is_active', currentItem.is_active);
      formData.append('type', currentItem.type);

      if (currentItem.id === null) {
        // 添加数据
        proxy.$axios.post("notify/", formData).then((res) => {
          state.notify.push(res.data);
          dialogVisible.value = false;
          ElMessage.success("添加成功")
        });
      } else {
        // 更新数据
        proxy.$axios.patch(`notify/${currentItem.id}/`, formData).then((res) => {
          const index = state.notify.findIndex((notify) => notify.id === currentItem.id);
          state.notify.splice(index, 1, res.data);
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