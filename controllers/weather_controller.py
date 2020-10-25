#!/usr/bin/python3
"""
parses the weather data from the api
and makes it available to the weather frame
"""
import os
import logging
import requests
from lib.utils import open_config_file
from lib.utils import TEMP_ADJUSTMENT_CONFIG_FILENAME, LOCATION_CONFIG_FILENAME, API_CONFIG_FILE_NAME
from api.obj.WeatherManager import WeatherManager

DIRNAME = os.path.dirname(__file__)

class WeatherController(object):
    """ Parses the weather data for the frame """
    def __init__(self):
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
        self.weather_config = open_config_file(LOCATION_CONFIG_FILENAME)
        self.temp_adjust_config = open_config_file(TEMP_ADJUSTMENT_CONFIG_FILENAME)
        self.api_config = open_config_file(API_CONFIG_FILE_NAME)
        self.weather_obj = None
        return

    def parse_weather(self):
        """ Parses the weather data """
        self.logger.debug("Parsing weather")
        self.location = self.weather_config["location"]
        formattedWeather = {}

        if self.api_config["use_local_api"]:
            #get weather data from local api
            formattedWeather = WeatherManager.get_weather_from_local_api(self.api_config["local_api_base"],
                                                            self.api_config["local_weather_endpoint"],
                                                            self.api_config["weather_req_url"], 
                                                            self.api_config["weather_api_token"], 
                                                            self.weather_config["latitude"], 
                                                            self.weather_config["longitude"], 
                                                            self.api_config["weather_lang"], 
                                                            self.api_config["weather_unit"], 
                                                            self.api_config["weather_exclude_list"])
        else:
            #get data directly from the weather api
            raw_weather = WeatherManager.get_weather_from_api(self.api_config["weather_req_url"], 
                                                                    self.api_config["weather_api_token"], 
                                                                    self.weather_config["latitude"], 
                                                                    self.weather_config["longitude"], 
                                                                    self.api_config["weather_lang"], 
                                                                    self.api_config["weather_unit"], 
                                                                    self.api_config["weather_exclude_list"])

            formattedWeather = WeatherManager.process_weather_results(raw_weather)

        self.weather_obj = formattedWeather

        #temp and formatted temp
        self.current_temp_int = int(formattedWeather['current_temp_int'])
        self.current_dew_point_int = int(formattedWeather['current_dew_point_int'])

        self.current_temp_formatted = formattedWeather['current_temp_formatted']

        #summary and forecast
        self.summary_text = formattedWeather['summary_text']

        self.forecast_text = formattedWeather['forecast_text']

        #weather icon
        icon_id = formattedWeather['icon_id']
        self.weather_icon = os.path.join(DIRNAME, "../assets/" + icon_id + "@4x.png")

        #humidity/dewpoint icon
        self.comfort_icon = self.get_comfort_emoji(self.temp_adjust_config["comfort_data"], self.current_temp_int, self.current_dew_point_int, formattedWeather['current_main'])
        
    def get_comfort_emoji(self, comfort_data, current_temp, current_dew_point, weather_main):
        icon = ""
        if weather_main == "Clear" or weather_main == "Clouds":
            if current_temp < comfort_data["cold_min_temp"]:
                icon = "cold"
            elif (comfort_data["perfect_temp_min"] <= current_temp <= comfort_data["perfect_temp_max"]) and current_dew_point <= comfort_data["comfortable_max_dew_point"]:
                icon = "smiling-face-with-heart"
            elif current_temp > comfort_data["comfortable_max_temp"]:
                icon = "hot"
            elif current_dew_point < comfort_data["comfortable_max_dew_point"]:
                icon = "happy"
            elif current_dew_point < comfort_data["sticky_max_dew_point"]:
                icon = "dew-point"
            else:
                icon = "hot"
        else:
            icon = "sad"
        
        return  os.path.join(DIRNAME, "../assets/" + icon + ".png")

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        """
        Static method for
        converting degrees kelvin to degrees fahrenheit
        """
        return 1.8 * (kelvin_temp - 273) + 32
