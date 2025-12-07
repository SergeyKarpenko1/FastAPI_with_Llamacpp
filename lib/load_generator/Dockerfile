FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Немного системных пакетов (опционально, но полезно)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Устанавливаем только httpx — больше ничего не нужно для генератора.
RUN pip install --no-cache-dir httpx

# Копируем ВСЁ репо, чтобы внутри были и lib, и handlers, и т.д.
COPY . .

# Запускаем модуль-воркер из пакета lib.workers
CMD ["python", "-m", "lib.workers.load_generator"]