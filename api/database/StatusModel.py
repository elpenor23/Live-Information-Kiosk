from database.database import db

class StatusModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String)
    last_set = db.Column(db.DateTime)
    number_of_calls = db.Column(db.Integer)
    average_seconds_between_calls = db.Column(db.Integer)