from flask_restful import Resource, reqparse
from datetime import datetime, timedelta
from database.database import db
from database.StatusModel import StatusModel

DATE_FORMAT = "%m/%d/%Y, %H:%M:%S"
MINUTES_TO_ADD = 0

class IndoorStatusResource(Resource):
  def __init__(self):
      self.setup_db()

  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument("data", type=str)
    args = parser.parse_args()
    data = args["data"]

    statuses = StatusModel.query.all()
    status = statuses[0]
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

    status.data = data
    status.last_set = current_time
    db.session.commit()
    
    return {"message": "Success!"}

  def get(self):
    statuses = StatusModel.query.all()
    status = statuses[0]
    return {"data": status.data, "last_set": status.last_set.strftime(DATE_FORMAT)}

  def setup_db(self):
    new_status = StatusModel(data = "XX", last_set = datetime.now())
    db.session.add(new_status)
    db.session.commit()
