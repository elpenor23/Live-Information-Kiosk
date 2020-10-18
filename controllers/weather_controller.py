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
    def __init__(self, weather_config, temp_adust_confg):
        """ initializes all of the weather data """
        #data for clothing calculations
        self.logger = logging.getLogger('kiosk_log')
        self.wind = ""
        self.precip = ""
        self.current_temp_int = 0

        #data for GUI updates
        self.current_temp_formatted = ""
        self.current_dew_point_int = 0
        self.summary_text = ""
        self.forecast_text = ""
        self.weather_icon = None
        self.comfort_icon = None
        self.location = ""

        #open config files
        self.weather_config = open_config_file(weather_config)
        self.temp_adjust_config = open_config_file(temp_adust_confg)
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
        self.current_dew_point_int = int(self.weather_obj['current']['dew_point'])

        #format temps for display
        current_temp = "%s%s " % (str(self.current_temp_int), degree_sign)
        min_temp = "%s%s" % (str(int(self.weather_obj["daily"][0]["temp"]["min"])), degree_sign)
        max_temp = "%s%s" % (str(int(self.weather_obj["daily"][0]["temp"]["max"])), degree_sign)

        self.current_temp_formatted = current_temp

        #summary and forecast
        self.summary_text = ("Today: " + self.weather_obj['current']['weather'][0]["description"] + "\n" + 
                            "Low: " + min_temp + " / High: " + max_temp)

        min_temp = "%s%s" % (str(int(self.weather_obj["daily"][1]["temp"]["min"])), degree_sign)
        max_temp = "%s%s" % (str(int(self.weather_obj["daily"][1]["temp"]["max"])), degree_sign)

        self.forecast_text = ("Tomorrow: " + self.weather_obj["daily"][1]["weather"][0]["description"] + 
                              "\nLow: " + min_temp + " / High: " + max_temp)

        #weather icon
        icon_id = self.weather_obj['current']["weather"][0]['icon']
        self.weather_icon = os.path.join(DIRNAME, "../assets/" + icon_id + "@4x.png")

        #humidity/dewpoint icon
        self.comfort_icon = self.get_comfort_emoji(self.temp_adjust_config["comfort_data"], self.current_temp_int, self.current_dew_point_int)
        
    def get_comfort_emoji(self, comfort_data, current_temp, current_dew_point):
        icon = ""
        if current_temp < comfort_data["cold_min_temp"]:
            icon = "freezing"
        elif (comfort_data["perfect_temp_min"] <= current_temp <= comfort_data["perfect_temp_max"]) and current_dew_point <= comfort_data["comfortable_max_dew_point"]:
            icon = "perfect"
        elif current_temp > comfort_data["comfortable_max_temp"]:
            icon = "gross"
        elif current_dew_point < comfort_data["comfortable_max_dew_point"]:
            icon = "decent"
        elif current_dew_point < comfort_data["sticky_max_dew_point"]:
            icon = "sticky"
        else:
            icon = "gross"
        
        return  os.path.join(DIRNAME, "../assets/" + icon + ".png")

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        """
        Static method for
        converting degrees kelvin to degrees fahrenheit
        """
        return 1.8 * (kelvin_temp - 273) + 32
