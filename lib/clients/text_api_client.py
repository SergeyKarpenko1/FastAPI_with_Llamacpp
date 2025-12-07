from __future__ import annotations

from typing import Any, Dict

import httpx


async def call_predict(
    client: httpx.AsyncClient,
    *,
    request_id: int,
    text: str,
    save: bool = False,
) -> Dict[str, Any]:
    """
    Вызов POST /predict нашего FastAPI-сервиса.

    Параметры:
      - client: общий AsyncClient с base_url, созданный снаружи
      - request_id: id, который уходит в JSON
      - text: текст, который надо отправить на генерацию
      - save: флаг, сохранять ли в БД (у нас сейчас False)

    Возвращает:
      - словарь, распарсенный из JSON-ответа сервера
    """
    payload = {
        "id": request_id,
        "text": text,
        "save": save,
    }

    response = await client.post("/predict", json=payload)

    # Если что-то пошло не так, выбрасываем исключение
    response.raise_for_status()

    return response.json()