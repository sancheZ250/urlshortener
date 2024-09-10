# Frontend Dockerfile

# Step 1: Используем официальный образ Node.js для Vue.js и Vite
FROM node:18

# Step 2: Устанавливаем рабочую директорию
WORKDIR /app

# Step 3: Копируем файлы package.json и package-lock.json и устанавливаем зависимости
COPY package*.json ./
RUN npm install

# Step 4: Копируем весь проект во фронтенд контейнер
COPY . .

# Step 5: Открываем порт 5173 для разработки
EXPOSE 5173

# Step 6: Запускаем Vite в режиме разработки
CMD ["npm", "run", "dev"]
