from database.database import db

class WeatherModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)
    last_set = db.Column(db.DateTime)