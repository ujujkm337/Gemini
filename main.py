import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Твой НОВЫЙ ключ
API_KEY = "AIzaSyDiiGeoRBtat0Hjt1YWgRzg6f2MyTwMnM8"

# Настройка модели
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Ошибка инициализации: {e}")

@app.route('/')
def home():
    return "✅ Gemini Proxy is Online!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_text = data.get('text', '')

        if not user_text:
            return jsonify({"reply": "Ошибка: Пустой запрос"}), 400

        # Запрос к Google
        response = model.generate_content(user_text)
        
        if response and response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "Gemini не смог сформировать ответ."}), 500

    except Exception as e:
        error_msg = str(e)
        print(f"Критическая ошибка: {error_msg}")
        # Возвращаем 200 с текстом ошибки, чтобы приложение в AIDE не вылетало по 500
        return jsonify({"reply": f"Ошибка сервера: {error_msg}"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
