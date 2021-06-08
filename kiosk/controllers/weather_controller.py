#!/usr/bin/python3
"""
parses the weather data from the api
and makes it available to the weather frame
"""
import os, json
import requests
from lib.utils import open_config_file
from lib.utils import ICON_CONFIG_FILENAME
from requests.exceptions import HTTPError 

DIRNAME = os.path.dirname(__file__)

class WeatherController(object):
    """ Parses the weather data for the frame """
    def __init__(self):
        """ initializes all of the weather data """
        #data for clothing calculations
        self.wind = ""
        self.precip = ""
        self.current_temp_int = 0

        #data for GUI updates
        self.current_weather_time = 0
        self.current_temp_formatted = ""
        self.current_feels_like_formatted = ""
        self.weather_time_formatted = ""
        self.current_dew_point_int = 0
        self.summary_text = ""
        self.forecast_text = ""
        self.weather_icon = None
        self.comfort_icon = None
        self.location = ""

        #open config files
        self.icon_config = open_config_file(ICON_CONFIG_FILENAME)
        self.weather_obj = None
        return

    def parse_weather(self, formattedWeather):
        """ Parses the weather data """

        self.weather_obj = formattedWeather

        if "current_temp_int" in formattedWeather:
            #temp and formatted temp
            self.current_temp_int = int(formattedWeather['current_temp_int'])
            self.current_dew_point_int = int(formattedWeather['current_dew_point_int'])
            self.current_temp_formatted = formattedWeather['current_temp_formatted']
            self.current_feels_like_formatted = formattedWeather['current_feels_like_formatted']
            self.current_weather_time = int(formattedWeather['weather_time'])
            self.weather_time_formatted = formattedWeather['weather_time_formatted']

            #summary and forecast
            self.summary_text = formattedWeather['summary_text']
            self.forecast_text = formattedWeather['forecast_text']

            #weather icon
            icon_id = formattedWeather['icon_id']
            self.weather_icon = os.path.join(DIRNAME, "../assets/" + icon_id + "@4x.png")

            #humidity/dewpoint icon
            self.comfort_icon = get_comfort_emoji(self.icon_config["comfort_data"], self.current_temp_int, self.current_dew_point_int, formattedWeather['current_main'])
        else:
            #temp and formatted temp
            self.current_temp_int = 69
            self.current_dew_point_int = 69
            self.current_temp_formatted = "69*"
            self.current_weather_time = 0

            #summary and forecast
            self.summary_text = "Houston: "
            self.forecast_text = "We have a problem..."

            #weather icon
            icon_id = "high-priority.png"
            self.weather_icon = os.path.join(DIRNAME, "../assets/" + icon_id)

            #humidity/dewpoint icon
            self.comfort_icon = get_comfort_emoji(self.icon_config["comfort_data"], self.current_temp_int, self.current_dew_point_int, "Clear")
        
def get_comfort_emoji(comfort_data, current_temp, current_dew_point, weather_main):
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

