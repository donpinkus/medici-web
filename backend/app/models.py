from . import db

class Drawing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False)  # Assuming Firebase user ID is a string
    drawing_data = db.Column(db.Text, nullable=False)
