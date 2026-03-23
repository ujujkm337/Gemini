from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Настройка Gemini
genai.configure(api_key="AIzaSyBR_jrIbU1NGxYpov6iNs-vLvly-7A5raY")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return "✅ Server is Online and Ready!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Пустой текст"}), 400
        
        prompt = data['text']
        print(f"Принято: {prompt}") # Появится в логах Render
        
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
    
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
