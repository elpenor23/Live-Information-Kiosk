from flask_restful import Resource, reqparse
from managers.MoonPhaseManager import MoonPhaseManager

class MoonPhaseResource(Resource):
  def get(self):
    data = MoonPhaseManager.moon_phase()
    return data

  
