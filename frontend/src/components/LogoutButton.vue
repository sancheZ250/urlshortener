<template>
    <button
      @click="logout"
      class="absolute top-4 right-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
    >
      Выйти
    </button>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router';
  import { useStore } from 'vuex';
  
  const router = useRouter();
  const store = useStore();
  
  const logout = () => {
    store.dispatch('logout');
    router.push({ name: 'login' });
  };
  </script>
  
  