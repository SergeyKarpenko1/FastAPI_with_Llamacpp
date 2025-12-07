from __future__ import annotations

import random
from typing import List


WORDS: List[str] = [
    "барсук",      
    "лось",        
    "енот",        
    "выдра",       
    "модель",
    "генератор",
    "запрос",
    "ответ",
    "токен",
    "батч",
    "сурок",      
    "косуля",      
    "инференс",
    "контекст",
]


def generate_random_text(min_words: int = 3, max_words: int = 8) -> str:
    """
    Генерация простой случайной фразы из слов WORDS.

    Выбираем случайное количество слов от min_words до max_words
    и склеиваем их через пробел.
    """
    n = random.randint(min_words, max_words)
    return " ".join(random.choice(WORDS) for _ in range(n))