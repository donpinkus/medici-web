from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
import firebase_admin
from firebase_admin import credentials
from .config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    CORS(app)

    cred = credentials.Certificate('./firebaseServiceAccountKey.json')
    
    # Only initialize the app if it does not already exist.
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred)

    with app.app_context():
        from . import routes  # Import routes
        db.create_all()

    return app
