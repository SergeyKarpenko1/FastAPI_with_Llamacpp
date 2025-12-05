from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from lib.handlers.schemas import PredictRequest, PredictResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan-контекст приложения.

    Здесь описываем:
    - что делаем при старте приложения (startup)
    - что делаем при остановке приложения (shutdown)

    В нашем случае:
    - при старте создаём экземпляр модели и кладём его в app.state
    - при остановке просто печатаем сообщение (ресурсов для закрытия пока нет)
    """
    print("LIFESPAN: запуск приложения, инициализируем модель TextGeneratorModel")
    app.state.mpdel = TextGeneratorModel()

    # сюда же позже можно добавить инициализацию БД, клиентов и т.д.
    yield
    
    print("LIFESPAN: приложение остановлено")
    # здесь можно закрывать соединения с БД, клиентов, пулов и т.п.

app = FastAPI(
    title="Text Generation Service",
    version="0.1.0",
    lifespan=lifespan
)

# -------------------- Middleware -------------------- #

@app.middleware("http")
async def simple_logger(request: Request, call_next):
    """
    Простое HTTP-middleware для логирования.

    Что делает:
    - перед обработкой запроса печатает метод и URL
    - после обработки печатает статус-код ответа

    """
    print(f"[Middleware] Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    print(f'[Middleware] Response status: {response.status_code}')
    return response

# -------------------- Эндпоинты -------------------- #

@app.get("/health")
async def healthcheck():
    """
    Healthcheck-эндпоинт.

    Используется для проверки, что сервис жив:
    - оркестраторами (Docker/Kubernetes),
    - балансировщиками,
    - мониторингом.

    Возвращает простой JSON со статусом.
    """
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
async def predict(request_data: PredictRequest):
    """
    Эндпоинт для генерации текста.

    Ожидает тело запроса в формате JSON (PredictRequest):
    {
      "id": <int>,
      "text": <str>,
      "save": <bool, опционально, по умолчанию false>
    }

    Логика:
    1. Берём уже инициализированную модель из app.state.model
       (инициализация была в lifespan).
    2. Вызываем у неё метод `predict` c request_data.text.
    3. Формируем ответ PredictResponse и возвращаем.

    Позже сюда добавим:
    - сохранение в БД при request_data.save == True.
    """

    model: TextGeneratorModel = app.state.__module__

    generated_text = model.predict(request_data.text)

    # TODO: при save=True сохранять запрос и ответ в БД
    # if request_data.save:
    #     await save_prediction(
    #         request_id=request_data.id,
    #         text=request_data.text,
    #         generated_text=generated_text,
    #     )

    response = PredictResponse(
        id=request_data.id,
        text=request_data.text,
        generated_text=generated_text,

    )

    return response


