from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from functools import wraps
import firebase_admin
from firebase_admin import credentials, auth, exceptions
import secrets
# Token generation
import jwt
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

db = SQLAlchemy(app)
login_manager = LoginManager(app)

cred = credentials.Certificate('./firebaseServiceAccountKey.json')
firebase_admin.initialize_app(cred)

# Define your routes and views here
@app.route('/')
def home():
    return jsonify({'message': 'Hello, World!'}), 200

@app.route('/protected', methods=['GET'])
def protected():
    id_token = request.headers.get('Authorization').split('Bearer ')[1]

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = auth.get_user(decoded_token['uid'])
        return jsonify({'message': 'Access granted', 'uid': uid}), 200
    except Exception as e:
        return jsonify({'message': 'Invalid token'}), 401


if __name__ == '__main__':
    app.run(debug=True)
