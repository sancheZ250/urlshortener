<template>
    <div class="mb-6">
      <label for="originalUrl" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Оригинальный URL</label>
      <input
        type="url"
        id="originalUrl"
        v-model="originalUrl"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        required
      />
      <button
        type="submit"
        class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
        @click.prevent="createShortUrl"
      >
        Создать сокращенный URL
      </button>
    </div>
  </template>
  
  <script setup>
  import { ref, defineEmits } from 'vue';
  import axios from 'axios';
  
  const emit = defineEmits(['shortUrlCreated']);
  const originalUrl = ref('');
  
  // Функция для создания сокращенного URL
  const createShortUrl = async () => {
    try {
      const response = await axios.post('/api/links/', { url: originalUrl.value });
      emit('shortUrlCreated', response.data); // Оповещаем родительский компонент о создании нового URL
      originalUrl.value = ''; // Очищаем поле ввода
    } catch (error) {
      console.error("Ошибка при создании URL:", error);
    }
  };
  </script>
  