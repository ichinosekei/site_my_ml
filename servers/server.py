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
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Ожидается JSON. Пример: {\"message\": \"привет\"}"}), 400
    user_message = data.get('message', '')
    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify({'response': 'Пустое сообщение'}), 400

    try:
        response_text = gemini.gemini(user_message)
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    if response_text.startswith("429"):
        return jsonify({"error": response_text}), 429
    if response_text.startswith("401"):
        return jsonify({"error": response_text}), 502
    if response_text.startswith("403"):
        return jsonify({"error": response_text}), 503

    return jsonify({'response': f"Модель ответила: {response_text}"}), 200



if __name__ == '__main__':
    app.run(debug=True)
