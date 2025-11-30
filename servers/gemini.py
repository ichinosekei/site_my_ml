import os
import logging
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
        "model": "google/gemini-2.0-flash-exp:free",
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

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к OpenRouter: {e}")
        return "Не удалось получить ответ от модели она бесплатная так что могут быть проблемы. Попробуйте позже."

    except (KeyError, IndexError, TypeError) as e:
        logger.error(f"Неожиданный формат ответа модели: {e}; raw response: {response.text if 'response' in locals() else 'нет'}")
        return "Модель вернула неожиданный ответ. Попробуйте переформулировать вопрос."
