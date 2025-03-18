<template>
  <div class="account-home-page">
    <header class="header">
      <nav>
        <div class="nav-container">
          <div class="nav-brand">
            <span class="username">欢迎，{{ username }}</span>
          </div>
          <ul class="nav-menu">
            <li class="nav-item">
              <router-link to="/home" class="nav-link">
                <i class="fas fa-home"></i> 首页
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/home/profile" class="nav-link">
                <i class="fas fa-user"></i> 个人资料
              </router-link>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link">
                <i class="fas fa-book"></i> 知识学习 <i class="fas fa-chevron-down"></i>
              </a>
              <ul class="dropdown-menu">
                <li>
                  <router-link to="/home/tang-dynasty" class="dropdown-item">
                    唐朝历史
                  </router-link>
                </li>
                <!-- 可以继续添加其他子菜单 -->
              </ul>
            </li>
            <li class="nav-item">
              <button @click="logout" class="logout-btn">
                <i class="fas fa-sign-out-alt"></i> 退出
              </button>
            </li>
          </ul>
        </div>
      </nav>
    </header>

    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'AccountHomePage',
  data() {
    return {
      username: ''
    };
  },
  created() {
    this.username = localStorage.getItem('username'); // 假设用户名存储在 localStorage 中
  },
  methods: {
    logout() {
      localStorage.removeItem('username'); // 清除用户名
      this.$router.push('/login'); // 重定向到登录页面
    }
  }
};
</script>

<style scoped>
/* 基础样式重置 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.account-home-page {
  min-height: 100vh;
  background: #f5f7fa;
}

/* 头部导航样式 */
.header {
  background: linear-gradient(135deg, #2c3e50, #34495e);
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.nav-brand .username {
  color: #ecf0f1;
  font-size: 1.2rem;
  font-weight: 500;
}

.nav-menu {
  display: flex;
  gap: 2rem;
  list-style: none;
}

.nav-link {
  color: #ecf0f1 !important;
  text-decoration: none;
  padding: 0.8rem 1rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

/* 下拉菜单样式 */
.dropdown {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 200px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(10px);
  transition: all 0.3s ease;
}

.dropdown:hover .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-item {
  color: #2c3e50 !important;
  padding: 0.8rem 1.2rem;
  text-decoration: none;
  display: block;
  transition: background 0.2s;
}

.dropdown-item:hover {
  background: #f8f9fa;
}

/* 退出按钮样式 */
.logout-btn {
  background: #e74c3c;
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logout-btn:hover {
  background: #c0392b;
  transform: translateY(-2px);
}

/* 主内容区域 */
.main-content {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 1rem;
  }

  .nav-menu {
    flex-wrap: wrap;
    justify-content: center;
  }

  .nav-link {
    padding: 0.6rem 0.8rem;
  }
}

/* 图标字体 */
.fas {
  font-size: 0.9rem;
}
</style>