from flask_restful import Resource, reqparse
from managers.IndoorStatusManager import IndoorStatusManager

class IndoorStatusResource(Resource):
  def __init__(self):
      IndoorStatusManager.setup_db()

  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument("data", type=str)
    args = parser.parse_args()
    data = args["data"]

    if data == None:
      message = {"message": "POST data not found"}, 500
    else:
      message = IndoorStatusManager.set_status(data)

    return message

  def get(self):
    data = IndoorStatusManager.get_status()
    return data

  
