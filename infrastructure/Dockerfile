FROM python:3.12-slim

WORKDIR /app

RUN apt-get update

COPY ../pyproject.toml ../poetry.lock  ./

RUN pip install poetry

# Устанавливаем зависимости
RUN poetry install --no-interaction --no-ansi --no-root

# Копируем папку api в контейнер
COPY ../api ./api

# Указываем рабочую директорию для Django
WORKDIR /app/api

# Команда для запуска сервера
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
