from __future__ import annotations
from typing import Any, Dict
import httpx


class PredictorClient:
    """
    Клиент для вызова POST /predict нашего FastAPI-сервиса.

    Параметры конструктора:
      - client: общий AsyncClient с base_url, созданный снаружи.

    Метод:
      - predict(): отправляет запрос на генерацию текста.

    Параметры predict():
      - request_id: id, который уходит в JSON
      - text: текст, который надо отправить на генерацию
      - save: флаг, сохранять ли в БД (у нас сейчас False)

    Возвращает:
      - словарь, распарсенный из JSON-ответа сервера
    """

    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def predict(
        self,
        *,
        request_id: int,
        text: str,
        save: bool = False,
    ) -> Dict[str, Any]:
        payload = {
            "id": request_id,
            "text": text,
            "save": save,
        }

        response = await self._client.post("/predict", json=payload)
        response.raise_for_status()
        return response.json()
