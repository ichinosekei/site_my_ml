from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    # Здесь можно интегрировать вашу ML модель.
    # Для примера возвращаем эхо-ответ.
    response_text = f"Модель ответила: Вы сказали '{user_message}'"
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
