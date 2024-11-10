from flask import Flask
from flask import render_template
from GPTPrompts import verify_community_guidelines
from flask import request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verify_community_guidelines', methods=['POST'])
def verify():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    text = data['text']
    try:
        # Call the verify_community_guidelines function with the provided text
        result = verify_community_guidelines(text)
        return jsonify(result)
    except Exception as e:
        # Log the exception and return a JSON error message
        print(f"Error in verify_community_guidelines: {e}")
        return jsonify({'error': 'An error occurred while processing the request', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

