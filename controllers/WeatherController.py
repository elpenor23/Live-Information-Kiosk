#!/usr/bin/python3
import json
import sys
import os
from lib.utils import get_weather, get_location, openConfigFile

# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter
dirname = os.path.dirname(__file__)

icon_lookup = {
    'clear-day': os.path.join(dirname, "../assets/Sun.png"),  # clear sky day
    'wind': os.path.join(dirname, "../assets/Wind.png"),   #wind
    'cloudy': os.path.join(dirname, "../assets/Cloud.png"),  # cloudy day
    'partly-cloudy-day': os.path.join(dirname, "../assets/PartlySunny.png"),  # partly cloudy day
    'rain': os.path.join(dirname, "../assets/Rain.png"),  # rain day
    'snow': os.path.join(dirname, "../assets/Snow.png"),  # snow day
    'snow-thin': os.path.join(dirname, "../assets/Snow.png"),  # sleet day
    'fog': os.path.join(dirname, "../assets/Haze.png"),  # fog day
    'clear-night': os.path.join(dirname, "../assets/Moon.png"),  # clear sky night
    'partly-cloudy-night': os.path.join(dirname, "../assets/PartlyMoon.png"),  # scattered clouds night
    'thunderstorm': os.path.join(dirname, "../assets/Storm.png"),  # thunderstorm
    'tornado': os.path.join(dirname, "../assests/Tornado.png"),    # tornado
    'hail': os.path.join(dirname, "../assests/Hail.png")  # hail
}

class WeatherController:
    def __init__(self, weatherConfig):
        #data for clothing calculations
        self.wind = ""
        self.timeOfDay = ""
        self.precip = ""
        self.currentTempInt = 0

        #data for GUI updates
        self.currentTempFormatted = ""
        self.summaryText = ""
        self.forecastText = ""
        self.weatherIcon = None
        self.location = ""

        #open config files
        self.weatherConfig = openConfigFile(weatherConfig)
        return
        
    def parse_weather(self):
        latitude = self.weatherConfig["latitude"]
        longitude = self.weatherConfig["longitude"]
        location = self.weatherConfig["location"]

        if latitude is None and longitude is None:
            loc = get_location()
            lat = loc['lat']
            lon = loc['lon']
            self.location = loc['location']
        else:
            lat = latitude
            lon = longitude
            self.location = location
        
        print("getting weather from parse_weather in WeatherController")
        self._weather_obj = get_weather(lat, lon)
        # print(self._weather_obj)

        #temp and formatted temp
        degree_sign= u'\N{DEGREE SIGN}'
        self.currentTempInt = int(self._weather_obj['currently']['temperature'])
        self.currentTempFormatted = "%s%s" % (str(self.currentTempInt), degree_sign)

        #summary and forecast
        self.summaryText = self._weather_obj['currently']['summary']
        self.forecastText = self._weather_obj["hourly"]["summary"]

        #weather icon
        icon_id = self._weather_obj['currently']['icon']
        if icon_id in icon_lookup:
            self.weatherIcon = icon_lookup[icon_id]

        self.timeOfDay = icon_id

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        return 1.8 * (kelvin_temp - 273) + 32