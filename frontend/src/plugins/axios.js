"use strict";

// import Vue from 'vue';
import axios from "axios";
import router from "@/router";
import store from "@/store";
import {ElMessage} from 'element-plus';

// Full config:  https://github.com/axios/axios#request-config
// axios.defaults.baseURL = "http://172.16.20.41:8000/v1/";
axios.defaults.baseURL = "http://127.0.0.1:8000/v1/";
// axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

let config = {
  // baseURL: process.env.baseURL || process.env.apiUrl || ""
  // timeout: 60 * 1000, // Timeout
  // withCredentials: true, // Check cross-site Access-Control
};

const _axios = axios.create(config);

_axios.interceptors.request.use(
    function(config) {
      // Do something before request is sent
      // 请求拦截器,让发送的每个请求携带jwt
      const token = localStorage.getItem('token');
      if (token) {
        // 这里后端限制了Bearer方法
        config.headers.common['Authorization'] = "Bearer "+token
      }
      return config;
    }
);

// Add a response interceptor
_axios.interceptors.response.use(
    function(response) {
      // Do something with response data
      return response;
    },
    function(error) {
      // Do something with response error
      // 响应错误拦截器，响应出现错误时，执行对应操作
      if (error.response.status === 401) {
        store.commit('logout');
        router.replace({name:"Login"})
        ElMessage.warning("会话已过期，请重新登录")
      }
      return Promise.reject(error);
    }
);

// 修改导出方式
export function installAxios(Vue) {
  Vue.config.globalProperties.$axios = _axios;
}
