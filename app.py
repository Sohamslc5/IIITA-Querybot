from flask import Flask, render_template, request, jsonify
import load_model
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['text']
    response = load_model.generate_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)