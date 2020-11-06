
from flask_restful import Resource
from flask import request
from enums.Enums import WeatherFetch
from managers.WeatherManager import WeatherManager

class WeatherResource(Resource):
    def __init__(self):
      WeatherManager.setup_db()

    def get(self):
        #setup arguments
        fetchType = WeatherFetch.NORMAL

        if 'type' in request.args:
            type = request.args.get("type")
            if type=="cached":
                fetchType = WeatherFetch.CACHEONLY
            elif type=="forcerefresh":
                fetchType = WeatherFetch.FORCEREFRESH
            
        if ("lat" in request.args and 'lon' in request.args):
            lat = request.args.get("lat")
            lon = request.args.get("lon")
        else:
            # status HTTP_428_PRECONDITION_REQUIRED 
            return {"message": "location missing"}, 428

        #get the weather
        data = WeatherManager.get_weather(fetchType, lat, lon)

        if "error" in data:
            return data, 500
        
        #return the data
        return data
