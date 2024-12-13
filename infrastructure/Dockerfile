FROM python:3.12-slim

WORKDIR /app

RUN apt-get update

COPY ../pyproject.toml ../poetry.lock ./

RUN pip install poetry

# Устанавливаем зависимости
RUN poetry install --no-dev

# Копируем папку api в контейнер
COPY ../api ./api

# Указываем рабочую директорию для Django
WORKDIR /app/api

# Команда для запуска сервера Django с миграцией
CMD ["sh", "-c", "poetry run python manage.py makemigrations --no-input && poetry run python manage.py migrate --no-input && poetry run python manage.py runserver 0.0.0.0:8000"]
