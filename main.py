import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Твой рабочий ключ
API_KEY = "AIzaSyDiiGeoRBtat0Hjt1YWgRzg6f2MyTwMnM8"

# Актуальный URL для Gemini 1.5 Flash
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

@app.route('/')
def home():
    return "✅ Gemini Bridge is Active"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_text = data.get('text', '')

        if not user_text:
            return jsonify({"reply": "Пустой запрос"}), 400

        # Формируем заголовки и тело запроса
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": API_KEY
        }
        
        payload = {
            "contents": [{
                "parts": [{"text": user_text}]
            }]
        }

        # Прямой запрос к Google
        response = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=30)
        result = response.json()

        # Если Google вернул ошибку (например, 404 или 403)
        if response.status_code != 200:
            error_msg = result.get('error', {}).get('message', 'Unknown Error')
            return jsonify({"reply": f"Google Error {response.status_code}: {error_msg}"}), 200

        # Извлекаем текст
        try:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": answer})
        except (KeyError, IndexError):
            return jsonify({"reply": f"Ошибка обработки: {str(result)}"}), 200

    except Exception as e:
        return jsonify({"reply": f"Ошибка сервера: {str(e)}"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
