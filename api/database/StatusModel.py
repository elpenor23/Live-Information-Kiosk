from database.database import db

class StatusModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String)
    last_set = db.Column(db.DateTime)