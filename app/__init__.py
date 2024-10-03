from flask import Flask
from app.app import app_blueprint  # Import the renamed blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(app_blueprint)  # Register the renamed blueprint
    return app
