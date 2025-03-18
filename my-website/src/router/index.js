import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage';
import LoginPage from '@/views/LoginPage';
import RegisterPage from '@/views/RegisterPage';
import AccountHomePage from '@/views/AccountHomePage';
import TangDynastyPage from '@/views/TangDynastyPage';
import ProfilePage from '@/views/ProfilePage';

const routerHistory = createWebHistory();

const router = createRouter({
  history: routerHistory,
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/login',
      name: 'LoginPage',
      component: LoginPage
    },
    {
      path: '/register',
      name: 'RegisterPage',
      component: RegisterPage
    },
    {
      path: '/home',
      name: 'AccountHomePage',
      component: AccountHomePage,
      children: [
        {
          path: 'profile',
          name: 'Profile',
          component: ProfilePage
        },
        {
          path: 'tang-dynasty',
          name: 'TangDynastyPage',
          component: TangDynastyPage
        }
      ]
    },
    {
      // Add this route to redirect to Django admin
      path: '/admin',
      beforeEnter() {
        window.location.href = 'http://127.0.0.1:8000/admin';
      }
    }
  ]
});

export default router;