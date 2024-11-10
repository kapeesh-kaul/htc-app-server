from flask import Flask
from flask_cors import CORS
from .routes import main_routes
from .openai_routes import openai_routes
import os

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))
    CORS(app)
    
    # Register the blueprints for routes
    app.register_blueprint(main_routes)
    app.register_blueprint(openai_routes, url_prefix='/openai')
    
    return app
