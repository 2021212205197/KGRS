import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'
import VueAxios from 'vue-axios'

// 创建一个 Axios 实例
const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 10000,
  // headers: { 'X-Custom-Header': 'foobar' }  // 如果不需要，可以移除自定义头部
})

// 可以在这里添加请求拦截器和响应拦截器
axiosInstance.interceptors.request.use(config => {
  // 在发送请求之前做些什么
  return config;
}, error => {
  // 对请求错误做些什么
  return Promise.reject(error);
});

axiosInstance.interceptors.response.use(response => {
  // 对响应数据做点什么
  return response;
}, error => {
  // 对响应错误做点什么
  return Promise.reject(error);
});

const app = createApp(App)
app.use(VueAxios, axiosInstance) // 使用 VueAxios 插件
app.use(router)
app.use(ElementPlus)
app.mount('#app')