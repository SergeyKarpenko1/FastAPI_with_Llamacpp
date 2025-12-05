from __future__ import annotations

import os

#
# Базовые настройки модели генерации текста (Meno-Tiny-0.1 GGUF).
#
# Ожидается, что GGUF-файл, например:
#   meno-tiny-0.1-q4_k_m.gguf
# будет лежать в ./models или другом каталоге проекта.
#
# Примеры чекапойнтов:
#   - bond005/meno-tiny-0.1-gguf
#   - itlwas/meno-tiny-0.1-Q4_K_M-GGUF
#   - AIronMind/meno-tiny-0.1-Q4_K_M-GGUF
#


# Путь до GGUF-модели Meno-Tiny-0.1 (Q4_K_M) внутри lib/models/weights
TEXT_GENERATOR_MODEL_PATH: str = os.getenv(
    "TEXT_GENERATOR_MODEL_PATH",
    "./lib/models/weights/meno-tiny-0.1-q4_k_m.gguf",
)

# Контекст. В модельной карточке для Q4_K_M-чекапойнта рекомендуют контекст 2048.  [oai_citation:3‡huggingface.co](https://huggingface.co/itlwas/meno-tiny-0.1-Q4_K_M-GGUF?utm_source=chatgpt.com)
TEXT_GENERATOR_CONTEXT_LENGTH: int = int(
    os.getenv("TEXT_GENERATOR_CONTEXT_LENGTH", "2048")
)

# Параметры генерации по умолчанию
TEXT_GENERATOR_MAX_TOKENS: int = int(
    os.getenv("TEXT_GENERATOR_MAX_TOKENS", "256")
)
TEXT_GENERATOR_TEMPERATURE: float = float(
    os.getenv("TEXT_GENERATOR_TEMPERATURE", "0.7")
)
TEXT_GENERATOR_TOP_P: float = float(
    os.getenv("TEXT_GENERATOR_TOP_P", "0.9")
)