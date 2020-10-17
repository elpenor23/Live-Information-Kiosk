#!/usr/bin/python3
"""
parses the weather data from the api
and makes it available to the weather frame
"""
import os
import logging
from lib.utils import get_weather, open_config_file

DIRNAME = os.path.dirname(__file__)

class WeatherController(object):
    """ Parses the weather data for the frame """
    def __init__(self, weather_config):
        """ initializes all of the weather data """
        #data for clothing calculations
        self.logger = logging.getLogger('kiosk_log')
        self.wind = ""
        self.precip = ""
        self.current_temp_int = 0

        #data for GUI updates
        self.current_temp_formatted = ""
        self.summary_text = ""
        self.forecast_text = ""
        self.weather_icon = None
        self.location = ""

        #open config files
        self.weather_config = open_config_file(weather_config)
        self.weather_obj = None
        return

    def parse_weather(self):
        """ Parses the weather data """
        self.logger.debug("Parsing weather")
        latitude = self.weather_config["latitude"]
        longitude = self.weather_config["longitude"]
        location = self.weather_config["location"]

        self.location = location

        self.weather_obj = get_weather(latitude, longitude)

        #temp and formatted temp
        degree_sign = u'\N{DEGREE SIGN}'
        self.current_temp_int = int(self.weather_obj['current']['temp'])
        self.current_temp_formatted = "%s%s" % (str(self.current_temp_int), degree_sign)

        #summary and forecast
        self.summary_text = (self.weather_obj['current']['weather'][0]["main"] + 
                            " - " + self.weather_obj['current']['weather'][0]["description"])

        self.forecast_text = (self.weather_obj["daily"][0]["weather"][0]["main"] +
                              "\n" + self.weather_obj["daily"][0]["weather"][0]["description"])

        #weather icon
        icon_id = self.weather_obj['current']["weather"][0]['icon']
        self.weather_icon = os.path.join(DIRNAME, "../assets/" + icon_id + "@4x.png")
        
    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        """
        Static method for
        converting degrees kelvin to degrees fahrenheit
        """
        return 1.8 * (kelvin_temp - 273) + 32
