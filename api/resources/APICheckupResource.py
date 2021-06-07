from flask_restful import Resource, reqparse
from managers.IndoorStatusManager import IndoorStatusManager
from managers.WeatherManager import WeatherManager

class APICheckupResource(Resource):
  def __init__(self):
      IndoorStatusManager.setup_db()

  def get(self):
    status_data = IndoorStatusManager.get_checkup_data()
    weather_data = WeatherManager.get_checkup_data()

    data = {
      "status_data": status_data,
      "weather_data": weather_data
    }
    if status_data is not None and weather_data is not None:
      if "error" in status_data or "error" in weather_data:
        return data, 500
      else:
        return data, 200
    else:
      return data, 500