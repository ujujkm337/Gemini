import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Твой ключ
API_KEY = "AIzaSyDiiGeoRBtat0Hjt1YWgRzg6f2MyTwMnM8"

# Настраиваем SDK
genai.configure(api_key=API_KEY)

# Выбираем модель. 
# В документации 2026 года 'gemini-1.5-flash' - это стандарт.
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "✅ Gemini Official SDK Bridge is Online"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_text = data.get('text', '')

        if not user_text:
            return jsonify({"reply": "Запрос пуст"}), 400

        # Генерация контента через официальный метод
        response = model.generate_content(user_text)
        
        # Проверка, не заблокировал ли Google ответ (Safety Ratings)
        if response.candidates:
            answer = response.text
            return jsonify({"reply": answer})
        else:
            return jsonify({"reply": "Google заблокировал ответ из-за настроек безопасности или пустого результата."}), 200

    except Exception as e:
        error_str = str(e)
        # Если всё же 404 или 403 - выводим понятный текст
        if "404" in error_str:
            return jsonify({"reply": "Ошибка 404: Модель не найдена. Попробуй сменить регион в Render на Frankfurt."}), 200
        if "location" in error_str.lower():
            return jsonify({"reply": "Ошибка региона: Google не работает в текущем регионе сервера. Смени регион в настройках Render на Frankfurt."}), 200
            
        return jsonify({"reply": f"Ошибка SDK: {error_str}"}), 200

if __name__ == "__main__":
    # Render передает порт через переменную окружения
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
