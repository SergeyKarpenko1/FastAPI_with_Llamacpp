from __future__ import annotations

from llama_cpp import Llama  # type: ignore

from lib.constants.models import (
    TEXT_GENERATOR_MODEL_PATH,
    TEXT_GENERATOR_CONTEXT_LENGTH,
    TEXT_GENERATOR_MAX_TOKENS,
    TEXT_GENERATOR_TEMPERATURE,
    TEXT_GENERATOR_TOP_P,
)
from .text_generator_model import TextGeneratorModel


def _create_llama_backend() -> Llama:
    """
    Создаёт и возвращает объект Llama (llama.cpp backend) для Meno-Tiny-0.1.

    Вся ответственность за:
    - путь к GGUF-файлу (TEXT_GENERATOR_MODEL_PATH)
    - размер контекста (TEXT_GENERATOR_CONTEXT_LENGTH)
    - возможные GPU-настройки (n_gpu_layers и т.п.)
    находится здесь.
    """
    print(
        "Meno-Tiny loader: инициализация Llama с GGUF моделью "
        f"по пути: {TEXT_GENERATOR_MODEL_PATH}"
    )

    llm = Llama(
        model_path=TEXT_GENERATOR_MODEL_PATH,
        n_ctx=TEXT_GENERATOR_CONTEXT_LENGTH,
        # При наличии GPU можно раскомментировать:
        # n_gpu_layers=-1,  # offload максимум слоёв на GPU
        # seed=0,
        # logits_all=False,
        # embedding=False,
    )

    return llm


def load_text_generator_model() -> TextGeneratorModel:
    """
    Публичная точка входа для загрузки Meno-Tiny-0.1 в виде TextGeneratorModel.

    На выходе — уже готовый объект TextGeneratorModel,
    который можно прокинуть в ModelClient.
    """
    backend = _create_llama_backend()
    model = TextGeneratorModel(backend=backend)

    print(
        "Meno-Tiny loader: модель готова "
        f"(max_tokens={TEXT_GENERATOR_MAX_TOKENS}, "
        f"temperature={TEXT_GENERATOR_TEMPERATURE}, "
        f"top_p={TEXT_GENERATOR_TOP_P})"
    )

    return model