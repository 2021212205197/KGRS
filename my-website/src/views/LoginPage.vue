<template>
  <div class="container">
    <div class="back-button">
      <button @click="navigateHome">返回</button>
    </div>
    <div class="login-box">
      <h1>登录</h1>
      <form @submit.prevent="login">
        <div class="input-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="username" required>
          <span v-if="usernameError" class="error">{{ usernameError }}</span>
        </div>
        <div class="input-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="password" required>
          <span v-if="passwordError" class="error">{{ passwordError }}</span>
        </div>
        <button type="submit">登录</button>
      </form>
      <div v-if="successMessage" class="success">{{ successMessage }}</div>
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
      usernameError: '',
      passwordError: '',
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    navigateHome() {
      this.$router.push('/');
    },
    async login() {
      this.clearErrors();

      if (this.username === '') {
        this.usernameError = '用户名不能为空';
      }

      if (this.password === '') {
        this.passwordError = '密码不能为空';
      }

      if (!this.usernameError && !this.passwordError) {
        try {
          const response = await axios.post('http://localhost:8000/zh-hans/api/login/', {
            username: this.username,
            password: this.password
          });

          if (response.status === 200) {
            localStorage.setItem('username', this.username); // 假设用户名存储在 localStorage 中
            this.successMessage = '登录成功！';
            setTimeout(() => {
              this.$router.push('/home'); // 登录成功后重定向到主页
            }, 1000);
          }
        } catch (error) {
          if (error.response) {
            this.errorMessage = error.response.data.message || '登录失败，请重试。';
          } else {
            this.errorMessage = '无法连接到服务器，请稍后重试。';
          }
        }
      }
    },
    clearErrors() {
      this.usernameError = '';
      this.passwordError = '';
      this.successMessage = '';
      this.errorMessage = '';
    }
  }
};
</script>

<style scoped>
body, html {
  height: 100%;
  margin: 0;
  font-family: Arial, sans-serif;
}

.container {
  background-image: url('@/assets/R.jpg');
  height: 100vh;
  width: 100vw;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  position: relative;
}

.back-button {
  position: absolute;
  top: 20px;
  left: 20px;
}

.back-button button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.back-button button:hover {
  background-color: #45a049;
}

.login-box {
  background: rgba(255, 255, 255, 0.8);
  padding: 40px;
  border-radius: 10px;
}

.login-box h1 {
  margin-bottom: 30px;
  font-size: 24px;
  color: #333;
}

.input-group {
  margin-bottom: 20px;
  text-align: left;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  font-size: 16px;
  color: #333;
}

.input-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.error {
  color: red;
  font-size: 14px;
  margin-top: 5px;
  display: block;
}

.success {
  color: green;
  font-size: 16px;
  margin-top: 20px;
}

button[type="submit"] {
  background-color: #4CAF50;
  color: white;
  padding: 15px 20px;
  margin-top: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

button[type="submit"]:hover {
  background-color: #45a049;
}
</style>