# FastAPI + llama.cpp (Meno-Tiny-0.1)

Небольшой сервис на FastAPI для генерации текста через `llama-cpp-python` (GGUF-чекапойнт Meno-Tiny-0.1). Сервис предоставляет REST API `/predict` и готов к запуску локально или в Docker.

## Стек
- FastAPI + Uvicorn
- llama-cpp-python (GGUF-модель)
- uv для управления зависимостями
- Ruff для форматирования/линта

## Структура проекта
- `lib/handlers/api.py` — точка входа FastAPI, middleware и эндпоинты `/health` и `/predict`.
- `lib/handlers/schemas.py` — Pydantic-схемы `PredictRequest` / `PredictResponse`.
- `lib/clients/model_client.py` — клиент для работы с моделью, использует генератор ниже.
- `lib/models/generator/loader.py` — загрузка GGUF-модели через `llama_cpp.Llama`.
- `lib/models/generator/text_generator_model.py` — обёртка над llama.cpp для генерации текста.
- `lib/constants/models.py` — настройки модели и параметры генерации (можно переопределить env-переменными).
- `Makefile` — удобные команды `run`, `format`, `lint`.
- `Dockerfile` — сборка образа со всеми зависимостями.
- Папки `data/`, `docs/`, `notebooks/`, `tests/` — заготовки под данные, документацию, эксперименты и тесты.

## Подготовка окружения
Требования: Python 3.12+, установленный `uv` (или pip), компилятор/билд-инструменты для сборки `llama-cpp-python` (gcc, cmake).

1. Клонируйте репозиторий и создайте виртуальное окружение:
   ```bash
   uv venv
   source .venv/bin/activate
   ```
2. Установите зависимости:
   ```bash
   uv pip install -r pyproject.toml
   ```
   Альтернатива без `uv`:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r pyproject.toml
   ```
3. Скачайте GGUF-чекапойнт Meno-Tiny-0.1 (например, `meno-tiny-0.1-q4_k_m.gguf`) и положите его в `lib/models/weights/` или задайте путь через переменную окружения:
   ```bash
   export TEXT_GENERATOR_MODEL_PATH=./lib/models/weights/meno-tiny-0.1-q4_k_m.gguf
   # Дополнительно можно переопределить:
   export TEXT_GENERATOR_CONTEXT_LENGTH=2048
   export TEXT_GENERATOR_MAX_TOKENS=256
   export TEXT_GENERATOR_TEMPERATURE=0.7
   export TEXT_GENERATOR_TOP_P=0.9
   ```

## Запуск
- Локально (uv + Makefile):
  ```bash
  make run
  # или без Makefile
  uv run --active uvicorn lib.handlers.api:app --reload --host 127.0.0.1 --port 8000
  ```
- Docker:
  ```bash
  docker build -t fastapi-llamacpp .
  # смонтируйте папку с весами, чтобы контейнер увидел GGUF
  docker run -p 8000:8000 \
    -v $(pwd)/lib/models/weights:/app/lib/models/weights \
    fastapi-llamacpp
  ```

## API
- `GET /health` — простой healthcheck (`{"status": "ok"}`).
- `POST /predict` — генерирует текст.
  - Тело запроса:
    ```json
    {"id": 1, "text": "Привет, что умеешь?", "save": false}
    ```
  - Ответ:
    ```json
    {"id": 1, "text": "Привет, что умеешь?", "generated_text": "<сгенерированный текст>"}
    ```
  - Пример запроса:
    ```bash
    curl -X POST http://127.0.0.1:8000/predict \
      -H "Content-Type: application/json" \
      -d '{"id":1,"text":"Привет, что умеешь?"}'
    ```

## Разработка
- Форматирование: `make format`
- Линт: `make lint` (или `make check`)
- Тесты пока не добавлены, заготовки лежат в `tests/`.
