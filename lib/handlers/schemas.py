from pydantic import BaseModel


class PredictRequest(BaseModel):
    """
    Входные данные для POST /predict.

    Поля:
    - id: идентификатор запроса/объекта (int)
    - text: исходный текст для модели (str)
    - save: флаг, нужно ли сохранять результат в БД (bool, по умолчанию False)
    """
    id: int
    text: str
    save: bool = False


class PredictResponse(BaseModel):
    """
    Ответ сервиса на POST /predict.

    Поля:
    - id: тот же id, что пришёл в запросе
    - text: исходный текст из запроса
    - generated_text: результат работы модели
    """
    id: int
    text: str
    generated_text: str