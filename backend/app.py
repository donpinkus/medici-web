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

# '''
# Pass the email and password in POST request body as JSON.
# '''
# @app.route('/login', methods=['POST'])
# def login():
#     email = request.json['email']
#     password = request.json['password']
#     try: 
#         user = auth.get_user_by_email(email)
#         auth.sign_in_with_email_and_password(email, password)
#         token = generate_token(user.uid)
#         return jsonify({'token': token}), 200
#     except auth.AuthError:
#         return jsonify({'message': 'Invalid email or passowrd.'}), 401
    
# @app.route('/signup', methods=['POST'])
# def signup():
#     email = request.json['email']
#     password = request.json['password']

#     # if there is no email or password, return an error about which is missing.
#     if not email or not password:
#         return jsonify({'message': 'Both email and password are required.'}), 400
    
#     try:
#         user = auth.create_user(email=email, password=password) # Firebase Admin SDK method
#         token = generate_token(user.uid)
#         return jsonify({'token': token, 'message': 'User created succesfully!'}), 200
#     except exceptions.FirebaseError as e:
#         if e.code == 'EMAIL_EXISTS':
#             return jsonify({'message': 'Email already exists'}), 400
#         else:
#             return jsonify({'message': 'An error occurred'}), 500

# def generate_token(user_id):
#     payload = {
#         'user_id': user_id,
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
#         'iat': datetime.datetime.utcnow()
#     }
#     token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
#     return token

# '''
# This decorator checks for the presence of a token in the 'Authorization' header. If the token is present, it verifies it using the auth.verify_id_token() method from Firebase Admin SDK. If the token is valid, it retrieves the user using auth.get_user() and passes the user object to the protected route.
# '''
# def token_required(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         token = request.headers.get('Authorization')
#         if not token:
#             return jsonify({'message': 'Token is missing'}), 401
#         try: 
#             decoded_token = auth.veryify_id_token(token)
#             current_user = auth.get_user(decoded_token['uid'])
#         except auth.InvalidIdTokenError:
#             return jsonify({'message': 'Invalid token'}), 401
#         return func(current_user, *args, **kwargs)
#     return decorated