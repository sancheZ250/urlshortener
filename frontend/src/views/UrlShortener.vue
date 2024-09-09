<template>
  <div class="max-w-3xl mx-auto p-6 bg-white shadow-md rounded-lg dark:bg-gray-800">
    <h1 class="text-2xl font-semibold text-gray-900 dark:text-white">Сокращение URL</h1>

    <ShortenUrlForm @shortUrlCreated="fetchUserLinks" />
    <UserLinksList :links="links" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ShortenUrlForm from '../components/ShortenUrlForm.vue';
import UserLinksList from '../components/UserLinkList.vue';
import axios from 'axios';

const links = ref([]);

// Функция для получения списка сокращенных URL
const fetchUserLinks = async () => {
  try {
    const response = await axios.get('/api/links/');
    links.value = response.data; // Обновляем список ссылок
  } catch (error) {
    console.error("Ошибка при получении ссылок:", error);
  }
};

// Получение ссылок при загрузке компонента
onMounted(() => {
  fetchUserLinks();
});
</script>
