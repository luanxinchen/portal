<template>
  <!--  container-->
  <div class="main">
    <div class="login-container">

      <div class="image-container">
        <img src="../assets/login.jpg" alt="login">
      </div>
      <!--    登录窗体-->
      <div class="login-box">
        <h2>ECUST</h2>
        <h2>管理后台登录</h2>
        <div class="tab-box-switch">
          <div style="width: 230px; height: 200px">
            <!--        账号登陆-->
            <div v-show="tabSelected===0">
              <el-form :model="userForm"
                       :rules="userRules"
                       ref="userRef"
                       @keyup.enter.native="doUserLogin">
                <el-form-item prop="username" :error="userError.username">
                  <el-input :prefix-icon="User" v-model="userForm.username" placeholder="用户名"/>
                </el-form-item>
                <el-form-item prop="password" :error="userError.password">
                  <el-input :prefix-icon="Unlock" type="password" show-password v-model="userForm.password"
                            placeholder="密码"/>
                </el-form-item>
              </el-form>
              <el-button type="primary" :style="{ width: '230px' }" @click="doUserLogin">登 录</el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, reactive, getCurrentInstance} from 'vue'
import {useStore} from 'vuex'
import {useRouter} from 'vue-router'
import {User, Unlock} from '@element-plus/icons-vue'
import {ElMessage} from 'element-plus'

const {proxy} = getCurrentInstance()
const store = useStore()
const router = useRouter()
// 初始化登录选项并默认选中
let tabSelected = ref(0)
const tabList = reactive(["账号密码登录"])


// 账号登陆
const userForm = reactive({
  username: '',
  password: '',
})

// 表单校验
const userRules = reactive({
  username: [
    {required: true, message: '请输入用户名', trigger: 'blur'},
    {min: 3, max: 16, message: '长度为3-8位', trigger: 'blur'},
  ],
  password: [
    {required: true, message: '请输入密码', trigger: 'blur'},
  ],
})

const userError = reactive({
  username: '',
  password: '',
})

/**
 * 账号登录
 */
function doUserLogin() {
  // 清除错误提示
  clearFormError(userError)

  // 获取表单校验
  proxy.$refs.userRef.validate((valid) => {
    // 校验失败
    if (!valid) {
      return false;
    }
    // 校验成功,向后端发送请求
    proxy.$axios.post(
        "login/",
        userForm
    ).then((res) => {
      // 获取响应体
      if (res.data.code === 0) {
        // 登录成功

        // 保存到vuex+持久化
        store.commit('login', res.data.results)

        // 跳转url
        router.replace({name: 'Site'})
        ElMessage.success("欢迎回来：" + res.data.results.name)


      } else {
        // 登录失败
        // 后端返回错误提示：
        if (res.data.code === 10006) {
          ElMessage.error(res.data.error.username[0])
        } else {
          ElMessage.error(res.data.error)
        }
      }
    })


  });

}

/**
 * 清除错误提示
 */
function clearFormError(errorDict) {
  for (let key in errorDict) {
    errorDict[key] = '';
  }
}


</script>

<style scoped>
.main {
  background-color: #ffffff;
  height: 100vh;
  display: flex;
  align-items: center;
}

.login-container {
  display: flex;
  justify-content: center;
  width: 800px;
  height: 400px;
  margin: 0 auto;
  align-items: center;
  border-radius: 30px;
  box-shadow: 0 2px 50px rgba(26, 26, 26, 0.1);
}


.image-container {
  flex: 60%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-container img {
  max-width: 100%;
  max-height: 350px;
}

.login-box {
  flex: 40%;
  height: 350px;
  width: 300px;
  margin: 60px 20px 20px 20px;
}

.demo-image {
  text-align: center;
}

.demo-image .block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 20%;
  box-sizing: border-box;
  vertical-align: top;
}

.demo-image .block:last-child {
  border-right: none;
}

.demo-image .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}

.tab-box-switch .switch-ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tab-box-switch .switch-ul li {
  display: inline-block;
  height: 60px;
  font-size: 16px;
  line-height: 60px;
  margin-right: 24px;
  cursor: pointer;
}

.tab-active {
  position: relative;
  color: #1a1a1a;
  font-weight: 600;
  font-synthesis: style;
}


.tab-active::before {
  display: block;
  position: absolute;
  bottom: 0;
  content: "";
  width: 100%;
  height: 3px;
  background-color: #0084ff;
}

.el-form-item {
  margin-top: 25px;
}
</style>