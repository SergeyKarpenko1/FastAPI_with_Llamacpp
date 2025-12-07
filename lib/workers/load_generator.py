from __future__ import annotations

import asyncio
from itertools import count

import httpx

from lib.clients.text_api_client import call_predict
from lib.utils.config import (
    TARGET_URL,
    CONCURRENCY,
    INTERVAL_SEC,
    REQUEST_TIMEOUT_SEC,
)
from lib.utils.random_text import generate_random_text


# Глобальный счётчик id для запросов
_id_counter = count(start=1)


def next_request_id() -> int:
    """
    Возвращает новый уникальный id для запроса.
    Используем itertools.count, чтобы не хранить состояние в БД.
    """
    return next(_id_counter)


async def worker_loop(
    worker_id: int,
    client: httpx.AsyncClient,
    interval: float,
) -> None:
    """
    Один воркер генерации запросов.

    В бесконечном цикле:
      1. генерирует случайный текст
      2. вызывает /predict через call_predict
      3. логирует результат (успех/ошибку)
      4. ждёт interval секунд
    """
    print(f"[worker {worker_id}] started, interval={interval}s")

    while True:
        req_id = next_request_id()
        text = generate_random_text()

        try:
            data = await call_predict(
                client,
                request_id=req_id,
                text=text,
                save=False,
            )
        except httpx.HTTPError as exc:
            print(f"[worker {worker_id}] HTTP ERROR for id={req_id}: {exc}")
        except Exception as exc:
            print(f"[worker {worker_id}] UNEXPECTED ERROR for id={req_id}: {exc}")
        else:
            generated = data.get("generated_text", "")
            short_generated = generated.replace("\n", " ")[:80]
            print(
                f"[worker {worker_id}] OK id={req_id} "
                f"text={text!r} -> generated={short_generated!r}"
            )

        await asyncio.sleep(interval)


async def main() -> None:
    """
    Главная асинхронная функция генератора.

    1. Логируем текущие настройки.
    2. Создаём один AsyncClient c base_url=TARGET_URL.
    3. Поднимаем CONCURRENCY воркеров через asyncio.create_task.
    4. Ждём их через asyncio.gather (они работают бесконечно).
    """
    print(
        f"[load_generator] starting with "
        f"TARGET_URL={TARGET_URL}, "
        f"CONCURRENCY={CONCURRENCY}, "
        f"INTERVAL_SEC={INTERVAL_SEC}, "
        f"REQUEST_TIMEOUT_SEC={REQUEST_TIMEOUT_SEC}"
    )

    timeout = httpx.Timeout(REQUEST_TIMEOUT_SEC)

    # Один клиент на все воркеры
    async with httpx.AsyncClient(
        base_url=TARGET_URL,
        timeout=timeout,
    ) as client:
        tasks = [
            asyncio.create_task(worker_loop(i + 1, client, INTERVAL_SEC))
            for i in range(CONCURRENCY)
        ]
        # gather будет "держать" процесс, пока контейнер не остановят
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[load_generator] stopped by user")