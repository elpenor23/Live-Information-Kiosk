from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
api = Api = Api(app)

DATE_FORMAT = "%m/%d/%Y, %H:%M:%S"
MINUTES_TO_ADD = 0

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////var/www/api/db/latch.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Latch(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  data = db.Column(db.String)
  last_set = db.Column(db.DateTime)

def setup_db():
  db.create_all()
  new_latch = Latch(data = "XX", last_set = datetime.now())
  db.session.add(new_latch)
  db.session.commit()

class LatchSet(Resource):
  def post(self, data):
    latches = Latch.query.all()
    record = latches[0]
    current_time = datetime.now()
    # This is for latching not sure if we need it so commenting it out
    # #if we are unsetting the latch we need to make sure that it has been
    # # at least 2 minutes since the last set
    # if set == 0:
    #   if record.is_set == 1:
    #     #we are trying to unset the latch
    #     deadline_date = record.last_set + timedelta(minutes = MINUTES_TO_ADD)
    #     if current_time < deadline_date:
    #       return

    record.data = data
    record.last_set = current_time
    db.session.commit()

    return {"message": "Success!"}

class LatchGet(Resource):
  def get(self):
    latches = Latch.query.all()
    latch = latches[0]
    return {"data": latch.data, "last_set": latch.last_set.strftime(DATE_FORMAT)}


api.add_resource(LatchSet, "/<string:data>")
api.add_resource(LatchGet, "/GET")
setup_db()

if __name__ == "__main__":
  #app.run(host="10.0.0.6", port="5000", debug=True)
  app.run()
