# Логика чтения ENV вынесена в один модуль – удобно и переиспользуемо.

from __future__ import annotations

import os


def get_env_str(name: str, default: str) -> str:
    value = os.environ.get(name)
    return value if value is not None else default


def get_env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def get_env_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


# Конфигурация для генератора нагрузочных запросов

TARGET_URL: str = get_env_str("TARGET_URL", "http://api:8000")
CONCURRENCY: int = get_env_int("CONCURRENCY", 3)
INTERVAL_SEC: float = get_env_float("INTERVAL_SEC", 2.0)
REQUEST_TIMEOUT_SEC: float = get_env_float("REQUEST_TIMEOUT_SEC", 60.0)
