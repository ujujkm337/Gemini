import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Твой рабочий ключ
API_KEY = "AIzaSyDiiGeoRBtat0Hjt1YWgRzg6f2MyTwMnM8"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# HTML-код страницы чата (всё в одном файле для простоты)
HTML_CHAT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini Web Chat</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #e5ddd5; display: flex; flex-direction: column; height: 100vh; margin: 0; }
        #chat-window { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; }
        .msg { max-width: 70%; margin-bottom: 10px; padding: 10px; border-radius: 10px; line-height: 1.4; }
        .user { align-self: flex-end; background-color: #dcf8c6; }
        .bot { align-self: flex-start; background-color: #fff; border: 1px solid #ccc; }
        #input-area { background: #eee; padding: 15px; display: flex; gap: 10px; }
        input { flex: 1; padding: 10px; border-radius: 20px; border: 1px solid #ccc; outline: none; }
        button { background: #075e54; color: white; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer; }
        button:disabled { background: #ccc; }
    </style>
</head>
<body>
    <div id="chat-window"></div>
    <div id="input-area">
        <input type="text" id="userInput" placeholder="Введите сообщение..." onkeypress="if(event.keyCode==13) send()">
        <button id="sendBtn" onclick="send()">Отправить</button>
    </div>

    <script>
        const chatWindow = document.getElementById('chat-window');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');

        async function send() {
            const text = userInput.value.trim();
            if (!text) return;

            appendMessage(text, 'user');
            userInput.value = '';
            sendBtn.disabled = true;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                const data = await response.json();
                appendMessage(data.reply, 'bot');
            } catch (e) {
                appendMessage("Ошибка связи с сервером", 'bot');
            } finally {
                sendBtn.disabled = false;
            }
        }

        function appendMessage(text, type) {
            const div = document.createElement('div');
            div.className = 'msg ' + type;
            div.innerText = text;
            chatWindow.appendChild(div);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # Отдаем HTML страницу при открытии ссылки
    return render_template_string(HTML_CHAT)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_text = data.get('text', '')
        
        if not user_text:
            return jsonify({"reply": "Вы ничего не ввели."}), 400

        # Прямой запрос к Gemini
        response = model.generate_content(user_text)
        
        if response and response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "Gemini промолчал..."})

    except Exception as e:
        return jsonify({"reply": f"Ошибка на сервере: {str(e)}"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
