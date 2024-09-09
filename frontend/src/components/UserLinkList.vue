<template>
  <div>
    <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Последние созданные URL</h2>
    <ul v-if="links.length" class="mt-4 space-y-2">
      <li v-for="link in links" :key="link.id" class="bg-gray-50 p-4 rounded-lg shadow">
        <p>Оригинальный URL: <a :href="link.url" target="_blank" class="text-blue-600">{{ link.url }}</a></p>
        <p>Сокращенный URL: 
          <a 
            :href="`/api/redirect/${link.short_url}/`" 
            target="_blank" 
            class="text-blue-600 cursor-pointer"
          >
            {{ link.short_url }}
          </a>
        </p>
        <p>Количество кликов: {{ link.clicks }}</p>
        <p>Дата регистрации: {{ formatDate(link.created_at) }}</p>
      </li>
    </ul>
    <p v-else class="text-gray-500">У вас нет сокращенных URL.</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  links: {
    type: Array,
    required: true,
  },
});

// Форматирование даты
const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};
</script>
