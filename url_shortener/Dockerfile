# Use the official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django app code into the container
COPY . /app/

# Expose the port that Django will run on
EXPOSE 8000

# Run migrations and create superuser automatically
CMD ["sh", "-c", "python manage.py migrate && python manage.py makemigrations && python manage.py createsuperuser --noinput && python manage.py runserver 0.0.0.0:8000"]
