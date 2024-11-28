FROM python:3.12-slim

WORKDIR /app

COPY ../pyproject.toml ./
COPY ../poetry.lock ./

RUN pip install poetry && poetry install

COPY ../api ./api

WORKDIR /app/api

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
