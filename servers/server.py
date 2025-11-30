from flask import Flask, request, jsonify, render_template
import gemini
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__, template_folder="../client/templates", static_folder="../client/static")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    response_text = f"Модель ответила: {gemini.gemini(user_message)}"
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
