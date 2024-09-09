<template>
  <div class="max-w-3xl mx-auto p-6 bg-white shadow-md rounded-lg dark:bg-gray-800">
    <h1 class="text-2xl font-semibold text-gray-900 dark:text-white">
      Панель администратора
    </h1>

    <!-- Форма для создания нового пользователя -->
    <div class="my-4 p-4 bg-gray-100 rounded-lg">
      <h2 class="text-xl font-semibold mb-2">Создать нового пользователя</h2>
      <form @submit.prevent="createUser">
        <div class="mb-4">
          <label for="username" class="block text-gray-700 dark:text-gray-300">Имя пользователя:</label>
          <input
            v-model="newUser.username"
            id="username"
            type="text"
            class="mt-1 block w-full p-2 border border-gray-300 rounded-lg"
            required
          />
        </div>
        <div class="mb-4">
          <label for="password" class="block text-gray-700 dark:text-gray-300">Пароль:</label>
          <input
            v-model="newUser.password"
            id="password"
            type="password"
            class="mt-1 block w-full p-2 border border-gray-300 rounded-lg"
            required
          />
        </div>
        <button
          type="submit"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Создать пользователя
        </button>
      </form>
    </div>

    <!-- Существующий код для отображения пользователей и ссылок -->
    <div v-if="users.length">
      <ul>
        <li v-for="user in users" :key="user.username" class="my-4">
          <div @click="toggleUserLinks(user.username)"
              class="cursor-pointer text-lg font-medium text-blue-600">
            {{ user.username }} (Нажмите, чтобы увидеть ссылки)
          </div>
          <button 
            @click.stop="deleteUser(user.id)"
            class="mt-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
          >
            Удалить пользователя
          </button>
          <button 
            @click.stop="deleteSelectedLinks(user.username)"
            class="mt-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
            :disabled="!selectedLinks[user.username].length"
          >
            Удалить выбранные ссылки
          </button>
          <ul v-if="openedUsers.includes(user.username)" class="mt-2 ml-4">
            <li v-for="link in user.links" :key="link.id" class="p-2 bg-gray-100 rounded-lg shadow-sm">
              <input 
                type="checkbox" 
                :id="'link-' + link.id"
                :value="link.id"
                v-model="selectedLinks[user.username]"
                class="mr-2"
              />
              <label :for="'link-' + link.id">
                <p>Оригинальный URL: <a :href="link.url" target="_blank" class="text-blue-600">{{ link.url }}</a></p>
                <p>Сокращенный URL: {{ link.short_url }}</p>
                <p>Количество кликов: {{ link.clicks }}</p>
                <p>Дата создания: {{ formatDate(link.created_at) }}</p>
              </label>
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <p v-else class="text-gray-500">Нет данных пользователей для отображения.</p>
  </div>
</template>

  
  
  
  <script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

const store = useStore();

const users = ref([]);
const openedUsers = ref([]);
const selectedLinks = ref({});
const newUser = ref({
  username: '',
  password: '',
});

// Получение списка пользователей и их ссылок
const fetchUserLinks = async () => {
  try {
    const response = await axios.get('/api/user-links/');
    users.value = response.data;
    // Инициализируем объект для хранения выбранных ссылок
    users.value.forEach(user => {
      selectedLinks.value[user.username] = [];
    });
  } catch (error) {
    console.error("Ошибка при получении списка пользователей:", error);
  }
};

// Функция для создания нового пользователя
const createUser = async () => {
  try {
    await axios.post('/api/auth/users/', newUser.value, {
      headers: {
        Authorization: `Token ${store.getters.getToken}`,
      },
    });
    // Очищаем форму и обновляем список пользователей
    newUser.value = { username: '', password: '' };
    fetchUserLinks();
  } catch (error) {
    console.error("Ошибка при создании пользователя:", error);
  }
};

// Функция для удаления пользователя
const deleteUser = async (userId) => {
  try {
    await axios.delete(`/api/users/${userId}/delete/`, {
      headers: {
        Authorization: `Token ${store.getters.getToken}`,
      },
    });
    // Обновляем список пользователей после удаления
    fetchUserLinks();
  } catch (error) {
    console.error("Ошибка при удалении пользователя:", error);
  }
};

// Функция для удаления выбранных ссылок
const deleteSelectedLinks = async (username) => {
  const linkIds = selectedLinks.value[username];
  if (linkIds.length === 0) return;

  try {
    await Promise.all(linkIds.map(id => axios.delete(`/api/links/${id}/`, {
      headers: {
        Authorization: `Token ${store.getters.getToken}`,
      },
    })));
    // Сбрасываем выбранные ссылки и обновляем список ссылок
    selectedLinks.value[username] = [];
    fetchUserLinks();
  } catch (error) {
    console.error("Ошибка при удалении ссылок:", error);
  }
};

// Функция для форматирования даты
const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

// Функция для отображения/скрытия ссылок пользователя
const toggleUserLinks = (username) => {
  if (openedUsers.value.includes(username)) {
    openedUsers.value = openedUsers.value.filter(user => user !== username);
  } else {
    openedUsers.value.push(username);
  }
};

// Загружаем данные при монтировании компонента
onMounted(() => {
  fetchUserLinks();
});
</script>

