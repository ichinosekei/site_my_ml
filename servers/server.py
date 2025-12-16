from flask import Flask, request, jsonify, render_template
from servers import gemini
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__, template_folder="../client/templates", static_folder="../client/static")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get('message', '')
    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify({'response': 'Пустое сообщение'}), 400
    response_text = f"Модель ответила: {gemini.gemini(user_message)}"
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
