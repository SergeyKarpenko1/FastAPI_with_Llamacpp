# lib/models/generator/text_generator_model.py

from __future__ import annotations

from typing import Any

from llama_cpp import Llama  # type: ignore


class TextGeneratorModel:
    """
    Обёртка над llama_cpp.Llama для модели Meno-Tiny-0.1.

    Здесь:
    - НЕТ логики загрузки файла GGUF с диска (это делает loader)
    - ТОЛЬКО интерфейс для генерации текста (predict)
    """

    def __init__(self, backend: Llama) -> None:
        """
        :param backend: уже инициализированный объект Llama.
        """
        self._backend = backend
        print("TextGeneratorModel: инициализирован (backend=llama.cpp, Meno-Tiny-0.1)")

    def predict(
        self,
        prompt: str,
        *,
        max_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> str:
        """
        Сгенерировать текст по prompt, используя llama.cpp backend.

        Возвращает строку с сгенерированным ответом без лишних пробелов.
        """
        result: dict[str, Any] = self._backend(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            # при необходимости можно добавить другие параметры:
            # stop=[...], repeat_penalty=..., top_k=..., и т.д.
        )

        # llama-cpp-python возвращает что-то вроде:
        # {
        #   "id": "...",
        #   "choices": [
        #       {
        #           "text": "...",
        #           ...
        #       }
        #   ],
        #   ...
        # }
        text = result["choices"][0]["text"]
        return text.strip()
