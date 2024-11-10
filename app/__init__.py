import os

from flask import Flask
from flask_cors import CORS
from mongoengine import connect

from pymongo import MongoClient
import pandas as pd

from .openai_routes import openai_routes
from .routes import main_routes
from .user_routes import user_routes


def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "../templates"),
    )
    CORS(app)

    # Connect to MongoDB using the MongoDB URI
    mongo_uri = os.getenv(
        "MONGO_URI"
    )  # Set your MongoDB URI as an environment variable
    connect(host=mongo_uri)

        

    # Register the blueprints for routes
    app.register_blueprint(main_routes)
    app.register_blueprint(openai_routes, url_prefix="/openai")
    app.register_blueprint(user_routes, url_prefix="/user")

    return app
