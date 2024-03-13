from flask import jsonify, request
from . import db, app
from .models import Drawing
from firebase_admin import auth

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
    
# Save drawing
@app.route('/api/save_drawing', methods=['POST'])
def save_drawing():
    id_token = request.headers.get('Authorization').split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
    except Exception as e:
        return jsonify({'message': 'Invalid token'}), 401

    data = request.json
    drawing = Drawing(user_id=uid, drawing_data=data['drawing_data'])
    db.session.add(drawing)
    db.session.commit()
    return jsonify({'message': 'Drawing saved'}), 200
