
from flask_restful import Resource
from flask import request
from datetime import datetime, timedelta
import json
from obj.WeatherManager import WeatherManager
from database.database import db
from database.WeatherModel import WeatherModel

DATE_FORMAT = "%m/%d/%Y, %H:%M:%S"
MINUTES_TO_ADD = 0

class WeatherResource(Resource):
    def __init__(self):
      self.setup_db()
      self.useLocalWeatherOnly = True

    def get(self):
        self.useLocalWeatherOnly = True
        #setup arguments
        if 'weather_api_url' in request.args:
            self.useLocalWeatherOnly = False
            self.api_url = request.args.get('weather_api_url')
            self.api_token = request.args.get('api_token')
            self.lat = request.args.get('lat')
            self.lon = request.args.get('lon')
            self.exclude = request.args.get('exclude')
            self.lang = request.args.get('lang')
            self.unit = request.args.get('unit')

        #get the weather
        data = self.get_weather()
        
        #return the data
        return {"data": data}
    
    def get_weather(self):
        """Gets the weather from the api in the apiConfig File"""
        # get weather
        allWeatherResults = WeatherModel.query.all()
        db_weather = allWeatherResults[0]
        current_time = datetime.now()

        #should we use the local data or refresh it?
        if not self.useLocalWeatherOnly and db_weather.last_set <= (current_time - timedelta(minutes = 1)):
            #get the weather from the api and save it locally
            weather = WeatherManager.get_weather_from_api(self.api_url, self.api_token, self.lat, self.lon, self.lang, self.unit, self.exclude)
            db_weather.data = json.dumps(weather)
            db_weather.last_set = current_time
            db.session.commit()
        else:
            #return weather we already have
            weather = json.loads(db_weather.data)

        return WeatherManager.process_weather_results(weather)

    def setup_db(self):
        new_status = WeatherModel(data = json.dumps(WeatherManager.create_empty_results()), last_set = (datetime.now() - timedelta(minutes = 60)))
        db.session.add(new_status)
        db.session.commit()