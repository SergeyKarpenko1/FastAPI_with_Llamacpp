FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 1) Устанавливаем инструменты сборки (gcc/g++ и т.п.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
 && rm -rf /var/lib/apt/lists/*

# 2) Устанавливаем uv
RUN pip install --no-cache-dir uv

# 3) Копируем весь проект (код + pyproject.toml + uv.lock + weights)
COPY . .

# 4) Ставим зависимости из pyproject.toml в системный Python
RUN uv pip install --system -r pyproject.toml

EXPOSE 8000

CMD ["uvicorn", "lib.handlers.api:app", "--host", "0.0.0.0", "--port", "8000"]