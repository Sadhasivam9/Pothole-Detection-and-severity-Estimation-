from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    app.config['RESULT_FOLDER'] = 'app/static/results'
    
    from .app import app as app_blueprint
    app.register_blueprint(app_blueprint)

    return app
