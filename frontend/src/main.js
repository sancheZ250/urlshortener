import { createApp } from 'vue';
import App from './App.vue';
import router from './routes';
import './style.css';
import axios from 'axios';
import store from './store'; // Подключаем store
import 'flowbite';

const app = createApp(App);
app.config.globalProperties.$axios = axios;

axios.interceptors.request.use(
  (config) => {
    const token = store.getters.getToken; // Берём токен из Vuex store через getter
    if (token) {
      config.headers['Authorization'] = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response.status === 401) {
      // Вызываем action logout из store
      store.dispatch('logout');
      
      // Дополнительно можно сделать редирект на страницу логина, если нужно
      router.push({ name: 'login' }); // 'login' — это имя вашего маршрута логина
    }
    return Promise.reject(error);
  }
);

app.use(router);
app.use(store);
app.mount('#app');
