import math
import re
from pathlib import Path


# Файл со словарём наиболее распространённых (слабых) паролей
COMMON_PASSWORDS_FILE = Path("common_passwords.txt")


def load_common_passwords():
    """Загружает словарь распространённых паролей из файла"""
    if COMMON_PASSWORDS_FILE.exists():
        with COMMON_PASSWORDS_FILE.open(encoding="utf-8") as f:
            return set(p.strip().lower() for p in f)
    return set()


# Загружаем словарь один раз при старте сервиса
COMMON_PASSWORDS = load_common_passwords()


def calculate_entropy(password: str) -> float:
    """Энтропия пароля"""
    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26
    if re.search(r"[A-Z]", password):
        charset += 26
    if re.search(r"[0-9]", password):
        charset += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        charset += 32

    if charset == 0:
        return 0.0

    return round(len(password) * math.log2(charset), 2)


def check_password(password: str):
    """
    Выполняет оценку надёжности пароля и формирует рекомендации
    по повышению уровня безопасности.
    """

    recommendations = []

    # Проверка по словарю распространённых паролей
    if password.lower() in COMMON_PASSWORDS:
        return {
            "уровень_надежности": "Слабый",
            "оценка": 0,
            "энтропия": 0.0,
            "рекомендации": [
                "Пароль является слишком распространённым и легко угадывается"
            ]
        }

    score = 0

    # Проверка длины пароля
    if len(password) >= 8:
        score += 1
    else:
        recommendations.append("Увеличьте длину пароля (минимум 8 символов)")

    if len(password) >= 12:
        score += 1

    # Проверка наличия строчных букв
    if re.search(r"[a-z]", password):
        score += 1
    else:
        recommendations.append("Добавьте строчные буквы")

    # Проверка наличия заглавных букв
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        recommendations.append("Добавьте заглавные буквы")

    # Проверка наличия цифр
    if re.search(r"[0-9]", password):
        score += 1
    else:
        recommendations.append("Добавьте цифры")

    # Проверка наличия специальных символов
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        recommendations.append("Добавьте специальные символы")

    # Итоговая оценка надёжности
    if score <= 2:
        strength = "Слабый"
    elif score <= 4:
        strength = "Средний"
    else:
        strength = "Сильный"

    return {
    "уровень_надежности": strength,
    "оценка": score,
    "энтропия": calculate_entropy(password),
    "рекомендации": recommendations
}
import math
import re
from pathlib import Path
from collections import Counter


COMMON_PASSWORDS_FILE = Path("common_passwords.txt")


def load_common_passwords():
    """
    Загружает словарь распространённых паролей.
    """
    if COMMON_PASSWORDS_FILE.exists():
        with COMMON_PASSWORDS_FILE.open(encoding="utf-8") as f:
            return set(p.strip().lower() for p in f)
    return set()


COMMON_PASSWORDS = load_common_passwords()


def has_too_many_repeats(password: str, threshold: float = 0.5) -> bool:
    """
    Проверяет, состоит ли пароль преимущественно
    из повторяющихся символов.
    """
    if not password:
        return False

    counts = Counter(password)
    most_common = counts.most_common(1)[0][1]

    return most_common / len(password) >= threshold


def calculate_entropy(password: str) -> float:
    """
    Вычисляет приближённую энтропию пароля.
    """
    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26
    if re.search(r"[A-Z]", password):
        charset += 26
    if re.search(r"[0-9]", password):
        charset += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        charset += 32

    if charset == 0:
        return 0.0

    return round(len(password) * math.log2(charset), 2)


def check_password(password: str):
    """
    Оценивает надёжность пароля и формирует рекомендации.
    """
    recommendations = []

    #Проверка по словарю распространённых паролей
    if password.lower() in COMMON_PASSWORDS:
        return {
            "strength": "Слабый",
            "score": 0,
            "entropy": 0.0,
            "recommendations": [
                "Пароль является слишком распространённым и легко угадывается"
            ]
        }

    #Проверка на повторяющиеся символы
    if has_too_many_repeats(password):
        return {
            "уровень_надежности": "Слабый",
            "оценка": 1,
            "энтропия": calculate_entropy(password),
            "рекомендации": [
                "Пароль содержит слишком много повторяющихся символов"
            ]
        }

    score = 0

    if len(password) >= 8:
        score += 1
    else:
        recommendations.append("Увеличьте длину пароля (минимум 8 символов)")

    if len(password) >= 12:
        score += 1

    if re.search(r"[a-z]", password):
        score += 1
    else:
        recommendations.append("Добавьте строчные буквы")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        recommendations.append("Добавьте заглавные буквы")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        recommendations.append("Добавьте цифры")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        recommendations.append("Добавьте специальные символы")

    if score <= 2:
        strength = "Слабый"
    elif score <= 4:
        strength = "Средний"
    else:
        strength = "Сильный"

    return {
        "уровень_надежности": strength,
        "оценка": score,
        "энтропия": calculate_entropy(password),
        "рекомендации": recommendations
    }
