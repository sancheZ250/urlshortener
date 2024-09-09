<template>
    <div class="max-w-md mx-auto p-6 bg-white shadow-md rounded-lg dark:bg-gray-800">
      <h1 class="text-2xl font-semibold text-gray-900 dark:text-white">Авторизация</h1>
      <form @submit.prevent="loginUser" class="mt-4 space-y-4">
        <div class="mb-6">
          <label for="username" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Имя пользователя</label>
          <input
            type="text"
            id="username"
            v-model="userData.username"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            required
          />
        </div>
        <div class="mb-6">
          <label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Пароль</label>
          <input
            type="password"
            id="password"
            v-model="userData.password"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            required
          />
        </div>
        <button
          type="submit"
          class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
        >
          Войти
        </button>
        <div v-if="loginError" class="text-red-600 dark:text-red-500">{{ loginError }}</div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useStore } from 'vuex';
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  
  const userData = ref({
    username: '',
    password: '',
  });
  const loginError = ref(null);
  
  const store = useStore();
  const router = useRouter();
  
  // Check if the user is already authenticated when the component is mounted
  onMounted(() => {
    if (store.getters.isAuthenticated) {
        if (store.getters.isAdmin) {
        router.push({ name: 'admin-panel' });
      } else {
        router.push({ name: 'url-shortener' });
      }
    }
  });
  
  const loginUser = async () => {
    try {
      const loginResponse = await axios.post("/api/auth/token/login/", userData.value);
      const auth_token = loginResponse.data.auth_token;
  
      const currentUserResponse = await axios.get("/api/auth/users/me/", {
        headers: {
          Authorization: `Token ${auth_token}`,
        },
      });
  
      //Check if user is an admin
      const response = await axios.get('/api/is-admin/', {
        headers: {
          Authorization: `Token ${auth_token}`,
        },
      });
      const is_user_admin = response.data.is_admin;
  
      // Store user info and isAdmin in Vuex
      store.dispatch('login', { 
        userId: currentUserResponse.data.id, 
        username: currentUserResponse.data.username, 
        token: auth_token,
        isAdmin: is_user_admin,  // Set isAdmin in store
      });
  
      //Redirect based on isAdmin
      if (is_user_admin) {
        router.push({ name: 'admin-panel' });
      } else {
        router.push({ name: 'url-shortener' });
      }
      
    } catch (error) {
      loginError.value = "Ошибка при входе. Проверьте имя пользователя и пароль.";
    }
  };
  </script>
  