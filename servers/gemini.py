import requests
import json

OPENROUTER_API_KEY = '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'

def gemini(question):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "<YOUR_SITE_URL>",
            "X-Title": "<YOUR_SITE_NAME>",
        },
        data=json.dumps({
            "model": "google/gemini-2.0-flash-001",  # Optional
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }))

    if response.status_code == 200:
        result = response.json()
        # print("Ответ от API:", result)
        # print(key, result['choices'][0]['message']['content'])
        return result['choices'][0]['message']['content']
    else:
        # print(key , "Ошибка:", response.status_code)
        # print("Сообщение:", response.text)
        return f' Вопрос {question}"Ошибка:", {response.status_code} "Сообщение:", {response.text} попробуй позже'