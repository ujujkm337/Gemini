import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Твой рабочий ключ
API_KEY = "AIzaSyDiiGeoRBtat0Hjt1YWgRzg6f2MyTwMnM8"

# Используем стабильную версию v1 вместо v1beta
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/')
def home():
    return "✅ Proxy is Ready"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_text = data.get('text', '')

        # Структура запроса для Gemini v1
        payload = {
            "contents": [{
                "parts": [{"text": user_text}]
            }]
        }

        # Отправляем запрос
        response = requests.post(GEMINI_URL, json=payload, timeout=30)
        result = response.json()

        # Проверка на ошибки от Google
        if response.status_code != 200:
            error_msg = result.get('error', {}).get('message', 'Unknown Error')
            return jsonify({"reply": f"Google Error {response.status_code}: {error_msg}"}), 200

        # Извлекаем ответ нейросети
        try:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": answer})
        except (KeyError, IndexLocal) as e:
            return jsonify({"reply": f"Ошибка парсинга ответа: {str(result)}"}), 200

    except Exception as e:
        return jsonify({"reply": f"Ошибка прокси: {str(e)}"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
