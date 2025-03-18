<template>
  <div class="container">
    <div class="back-button">
      <button @click="navigateHome">返回</button>
    </div>
    <div class="register-box">
      <h1>注册</h1>
      <form @submit.prevent="register">
        <div class="input-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="username" required>
          <span v-if="usernameError" class="error">{{ usernameError }}</span>
        </div>
        <div class="input-group">
          <label for="email">邮箱</label>
          <input type="email" id="email" v-model="email" required>
          <span v-if="emailError" class="error">{{ emailError }}</span>
        </div>
        <div class="input-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="password" required>
          <span v-if="passwordError" class="error">{{ passwordError }}</span>
        </div>
        <button type="submit">注册</button>
      </form>
      <div v-if="successMessage" class="success">{{ successMessage }}</div>
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterPage',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      usernameError: '',
      emailError: '',
      passwordError: '',
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    navigateHome() {
      this.$router.push('/');
    },
    async register() {
      this.clearErrors();

      if (this.username.length < 3) {
        this.usernameError = '用户名不能少于3位';
      }

      const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      if (!emailPattern.test(this.email)) {
        this.emailError = '邮箱格式不正确';
      }

      if (this.password.length < 6) {
        this.passwordError = '密码不能少于6位';
      }

      if (!this.usernameError && !this.emailError && !this.passwordError) {
        try {
          const response = await axios.post('http://localhost:8000/zh-hans/api/register/', {
            username: this.username,
            email: this.email,
            password: this.password
          });

          if (response.status === 201) {
            this.successMessage = '注册成功！';
            this.username = '';
            this.email = '';
            this.password = '';
          }
        } catch (error) {
          if (error.response && error.response.data && error.response.data.message === '用户名已存在') {
            this.usernameError = '用户名已存在';
          } else {
            this.errorMessage = error.response && error.response.data && error.response.data.message || '注册失败，请重试。';
          }
        }
      }
    },
    clearErrors() {
      this.usernameError = '';
      this.emailError = '';
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

.register-box {
  background: rgba(255, 255, 255, 0.8);
  padding: 40px;
  border-radius: 10px;
}

.register-box h1 {
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