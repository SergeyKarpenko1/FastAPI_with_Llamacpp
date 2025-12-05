from __future__ import annotations

from lib.models.generator.loader import load_text_generator_model
from lib.models.generator.text_generator_model import TextGeneratorModel
from lib.constants.models import (
    TEXT_GENERATOR_MAX_TOKENS,
    TEXT_GENERATOR_TEMPERATURE,
    TEXT_GENERATOR_TOP_P,
)


class ModelClient:
    """
    Клиент для работы с моделью Meno-Tiny-0.1.

    Остальная часть приложения (FastAPI-хэндлеры, воркеры и т.д.)
    должна работать с моделью через этот класс, а не напрямую
    с llama_cpp или TextGeneratorModel.
    """

    def __init__(self, model: TextGeneratorModel | None = None) -> None:
        # Можно передать уже созданную модель (для тестов/DI),
        # или позволить клиенту загрузить модель самостоятельно.
        if model is None:
            self._model = load_text_generator_model()
        else:
            self._model = model

    def generate_text(
        self,
        text: str,
        *,
        max_tokens: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
    ) -> str:
        """
        Основной публичный метод клиента.

        Позволяет при вызове переопределить параметры генерации,
        но по умолчанию использует значения из lib.constants.models.
        """
        return self._model.predict(
            text,
            max_tokens=max_tokens or TEXT_GENERATOR_MAX_TOKENS,
            temperature=temperature or TEXT_GENERATOR_TEMPERATURE,
            top_p=top_p or TEXT_GENERATOR_TOP_P,
        )
