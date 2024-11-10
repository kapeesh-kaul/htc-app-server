from flask import Flask
from flask import render_template
from GPTPrompts import verify_community_guidelines, process_pronouns
from flask import request, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    
@app.route('/process_pronouns', methods=['POST'])
def process_pronouns_endpoint():
    data = request.json

    # Validate request data
    if not data or 'message_input' not in data or 'users' not in data:
        return jsonify({'error': 'Invalid input. Please provide both "message_input" and "users".'}), 400
    
    message_input = data['message_input']
    users = data['users']

    try:
        # Process the message using pronoun replacement
        result = process_pronouns(message_input, users)
        return jsonify(result)
    except Exception as e:
        # Handle errors and provide a response
        print(f"Error in process_pronouns: {e}")
        return jsonify({'error': 'An error occurred while processing the request', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

