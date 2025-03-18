<template>
  <div class="profile-page">
    <h1>个人资料</h1>
    <p>用户名: {{ username }}</p>
    <p>邮箱: {{ email }}</p>
  </div>
</template>

<script>
export default {
  name: 'ProfilePage',
  data() {
    return {
      username: '默认用户名',
      email: 'default@example.com'
    };
  }
};
</script>

<style scoped>
.profile-page {
  padding: 20px;
  text-align: center;
}

.profile-page h1 {
  font-size: 2em;
  margin-bottom: 20px;
}

.profile-page p {
  font-size: 1.2em;
  margin: 10px 0;
}
</style>