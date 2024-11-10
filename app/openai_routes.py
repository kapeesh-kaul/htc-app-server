from flask import Blueprint, request, jsonify
from GPTPrompts import verify_community_guidelines, process_pronouns, moderate_chat

openai_routes = Blueprint('openai_routes', __name__)

@openai_routes.route('/verify_community_guidelines', methods=['POST'])
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

@openai_routes.route('/process_pronouns', methods=['POST'])
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

@openai_routes.route('/moderate_chat', methods=['POST'])
def moderate_chat_endpoint():
    data = request.json

    # Validate input
    if not data or 'messages' not in data:
        return jsonify({'error': 'Invalid input. Please provide a "messages" field.'}), 400

    messages = data['messages']

    try:
        # Call the moderate_chat function with the provided messages
        result = moderate_chat(messages)
        return jsonify(result)
    except Exception as e:
        # Handle errors and provide a response
        print(f"Error in moderate_chat: {e}")
        return jsonify({'error': 'An error occurred while processing the request', 'details': str(e)}), 500
