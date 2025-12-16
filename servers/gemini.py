import os
import logging
import time

import requests


os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/gemini.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


MAX_QUESTION_LEN = 200
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3-nano-30b-a3b:free")

def gemini(question: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.error("OPENROUTER_API_KEY не задан.")
        raise RuntimeError("OPENROUTER_API_KEY не задан. Установи переменную окружения OPENROUTER_API_KEY.")

    if not isinstance(question, str):
        logger.warning(f"Невалидный тип question: {type(question)}")
        return "Ошибка: вопрос должен быть текстом."

    question = question.strip()

    if len(question) == 0:
        logger.info("Пустой вопрос от пользователя.")
        return "Пожалуйста, напишите вопрос, а не пустую строку"

    if len(question) > MAX_QUESTION_LEN:
        logger.info(
            f"Слишком длинный вопрос ({len(question)} символов, лимит {MAX_QUESTION_LEN}). Вопрос обрезан."
        )
        return f"Слишком длинный вопрос (максимум {MAX_QUESTION_LEN} символов)."



    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://example.com",  # TODO:  URL  сайта
        "X-Title": "My ML Study Project",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": question,
            }
        ],
    }

    logger.info(f"Отправка запроса к модели: model={payload['model']}, len(question)={len(question)}")

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        data = response.json()
        answer = data["choices"][0]["message"]["content"]

        logger.info(f"Успешный ответ от модели, длина ответа: {len(answer)} символов")

        return answer


    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else None
        body = e.response.text if e.response is not None else ""
        logger.warning(f"OpenRouter HTTP {status}: {body[:500]}")
        if status == 429:
            logger.warning("429: ждем 2 сек и пробуем еще раз")
            time.sleep(2)
            r2 = requests.post(url, headers=headers, json=payload, timeout=30)
            if r2.status_code == 200:
                data = r2.json()
                return data["choices"][0]["message"]["content"]
            return "429 Too Many Requests: подожди 10–30 секунд и попробуй ещё раз."
        if status == 401:
            return "401 Unauthorized: OPENROUTER_API_KEY."
        return f"Ошибка OpenRouter (HTTP {status}). Попробуйте позже."

    except requests.exceptions.Timeout:
        logger.error("Timeout при запросе к OpenRouter")
        return "Таймаут: сервис ИИ отвечает слишком долго. Попробуйте позже."

    except requests.exceptions.RequestException as e:
        logger.error(f"Сетевая ошибка при запросе к OpenRouter: {e}")
        return "Сетевая ошибка при обращении к сервису ИИ. Попробуйте позже."