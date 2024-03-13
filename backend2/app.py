from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import firebase_admin
from firebase_admin import credentials, auth, firestore
import os

app = Flask(__name__)

# CORS
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# Auth stuff
cred = credentials.Certificate("./firebaseServiceAccountKey.json")  # Update this path
firebase_admin.initialize_app(cred)

def check_token(f):
    def wrap(*args, **kwargs):
        id_token = request.headers.get("Authorization").split("Bearer ")[1]
        print(id_token)

        try:
            # Verify Firebase Auth ID Token
            decoded_token = auth.verify_id_token(id_token)
            print("DECODED!")
            user_id = decoded_token['uid']  # Note: Changed 'user_id' to 'uid'
        except:
            return jsonify({"message": "Invalid token"}), 403
        return f(user_id, *args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# DB stuff
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

# Models
class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120), nullable=False)
    image_data = db.Column(db.Text, nullable=False)

# Routes
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/artwork', methods=['POST'])
@check_token
def create_artwork(user_id):
    data = request.get_json()
    new_artwork = Artwork(user_id=user_id, image_data=data['image_data'])
    db.session.add(new_artwork)
    db.session.commit()
    return jsonify({"message": "Artwork created", "id": new_artwork.id }), 201

@app.route('/api/artwork/<int:artwork_id>', methods=['PUT'])
@check_token
def update_artwork(user_id, artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    if artwork.user_id != user_id:
        return jsonify({"message": "Unauthorized"}), 403
    data = request.get_json()
    artwork.image_data = data['image_data']
    db.session.commit()
    return jsonify({"message": "Artwork updated", "id": artwork.id }), 200

# Main app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=4000)
    