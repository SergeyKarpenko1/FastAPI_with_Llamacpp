.PHONY: run format lint check

APP_MODULE := lib.handlers.api:app
# Если появятся отдельные файлы в корне, можно добавить:
# CODE_PATHS := lib tests main.py test.py
CODE_PATHS := lib tests

run:
	# Запуск FastAPI-приложения через uv
	uv run --active uvicorn $(APP_MODULE) --reload --host 127.0.0.1 --port 8000

format:
	# Автоформатирование кода ruff'ом (через uv run)
	uv run --active ruff format $(CODE_PATHS)

lint:
	# Линтинг кода ruff'ом (через uv run)
	uv run --active ruff check $(CODE_PATHS)

check: lint