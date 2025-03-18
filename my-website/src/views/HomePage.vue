<template>
  <div class="container">
    <div class="login-box">
      <h1>欢迎来到个性化学习推荐系统</h1>
      <div class="buttons">
        <button @click="navigateTo('/login')">登录</button>
        <button @click="navigateTo('/register')">注册</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  methods: {
    navigateTo(route) {
      this.$router.push(route);
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

.buttons button {
  background-color: #4CAF50;
  color: white;
  padding: 15px 20px;
  margin: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.buttons button:hover {
  background-color: #45a049;
}
</style>