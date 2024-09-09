import { createRouter, createWebHistory } from 'vue-router';

// Динамический импорт компонентов
const Login = () => import('../components/Login.vue');
const UrlShortener = () => import('../views/UrlShortener.vue');
const AdminPanel = () => import('../views/AdminPanel.vue');

const routes = [
  { path: '/', component: Login, name: 'login' }, // Маршрут для страницы авторизации
  { path: '/url-shortener', component: UrlShortener, name: 'url-shortener' }, // Маршрут для страницы сокращения URL
  { path: '/admin-dashboard', component: AdminPanel, name: 'admin-panel' }, // Маршрут для страницы сокращения URL
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
