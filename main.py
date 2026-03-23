import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Твой рабочий ключ
API_KEY = "AIzaSyDiiGeoRBtat0Hjt1YWgRzg6f2MyTwMnM8"

# Используем v1beta и полный путь к модели
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/')
def home():
    return "✅ Proxy is Ready"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_text = data.get('text', '')

        if not user_text:
            return jsonify({"reply": "Введите текст запроса"}), 400

        # Структура запроса
        payload = {
            "contents": [{
                "parts": [{"text": user_text}]
            }]
        }

        # Отправляем запрос к Google
        response = requests.post(GEMINI_URL, json=payload, timeout=30)
        result = response.json()

        # Если Google вернул ошибку
        if response.status_code != 200:
            error_message = result.get('error', {}).get('message', 'Unknown Error')
            return jsonify({"reply": f"Google Error {response.status_code}: {error_message}"}), 200

        # Безопасное извлечение текста
        try:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": answer})
        except (KeyError, IndexLocal, TypeError):
            return jsonify({"reply": f"Ошибка структуры ответа: {str(result)}"}), 200

    except Exception as e:
        return jsonify({"reply": f"Ошибка сервера: {str(e)}"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
