FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Устанавливаем uv
RUN pip install --no-cache-dir uv

# Копируем проект целиком (код + pyproject.toml + uv.lock + weights)
COPY . .

# Ставим зависимости из pyproject.toml в системный Python контейнера
# (по сути замена ручного pip install списка)
RUN uv pip install --system -r pyproject.toml

EXPOSE 8000

CMD ["uvicorn", "lib.handlers.api:app", "--host", "0.0.0.0", "--port", "8000"]