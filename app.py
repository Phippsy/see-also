from flask import Flask, render_template, request, jsonify
import json
from gpt import complete_structured

app = Flask(__name__)

# Load the prompt used for the developer message
try:
    with open('prompts/related.txt', 'r') as f:
        RELATED_PROMPT = f.read()
except FileNotFoundError:
    RELATED_PROMPT = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    concepts = None
    user_text = ''
    if request.method == 'POST':
        user_text = request.form.get('text', '')
        if user_text:
            raw_response = complete_structured(user_text, developer_message=RELATED_PROMPT)
            data = json.loads(raw_response)
            concepts = data.get('concepts', [])
    return render_template('index.html', concepts=concepts, user_text=user_text)


@app.route('/expand', methods=['POST'])
def expand():
    data = request.get_json(silent=True) or {}
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'no text provided'}), 400
    raw_response = complete_structured(text, developer_message=RELATED_PROMPT)
    return jsonify(json.loads(raw_response))

if __name__ == '__main__':
    app.run(debug=True)
