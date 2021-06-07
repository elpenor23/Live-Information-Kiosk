from database.database import db

class WeatherModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)
    last_call = db.Column(db.DateTime)
    number_of_calls = db.Column(db.Integer)
    average_seconds_between_calls = db.Column(db.Integer)
    last_set = db.Column(db.DateTime)
    number_of_resets = db.Column(db.Integer)
    average_seconds_between_resets = db.Column(db.Integer)