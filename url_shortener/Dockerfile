# Backend Dockerfile

# Step 1: Используем официальный образ Python для Django
FROM python:3.12

# Step 2: Устанавливаем рабочую директорию
WORKDIR /app

# Step 3: Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Копируем весь проект в контейнер
COPY . .

# Step 5: Открываем порт 8000 для разработки Django
EXPOSE 8000

# Step 7: Запускаем миграции и сервер разработки Django
CMD ["sh", "-c", "python manage.py migrate && python manage.py createsuperuser --noinput && python manage.py runserver 0.0.0.0:8000"]
