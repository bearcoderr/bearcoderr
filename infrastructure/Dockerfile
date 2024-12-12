# Используем базовый образ Python 3.12
FROM python:3.12-slim

# Обновляем пакеты и устанавливаем зависимости для Poetry
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
COPY ../pyproject.toml ../poetry.lock ./
RUN pip install poetry

# Копируем папку api в контейнер
COPY ../api ./api

# Указываем рабочую директорию для Django
WORKDIR /app/api

# Убеждаемся, что папка существует, и очищаем старые миграции, оставляя __init__.py
RUN mkdir -p ./src/models/migrations/ && \
    find ./src/models/migrations/ -type f ! -name "__init__.py" -delete

# Проверяем, что manage.py есть в папке
RUN ls -l /app/api/manage.py

# Создаём и применяем миграции
RUN poetry run python manage.py makemigrations --noinput && \
    poetry run python manage.py migrate --noinput

# Команда для запуска Django через Poetry
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
