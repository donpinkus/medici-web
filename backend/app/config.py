import secrets

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False