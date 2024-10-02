#!/usr/bin/python3
"""
parses the weather data from the api
and makes it available to the weather frame
"""
import os
import re
from datetime import datetime, timedelta
from lib.utils import open_config_file, get_api_data
from lib.utils import ICON_CONFIG_FILENAME, API_CONFIG_FILE_NAME, LOCATION_CONFIG_FILENAME

DIRNAME = os.path.dirname(__file__)
DATE_FORMAT = "%m/%d/%Y %H:%M:%S"
#TODO: MAKE Objects for the data the controller should not be and object that holds data
class WeatherController(object):
    """ Parses the weather data for the frame """
    def __init__(self):
        """ initializes all of the weather data """
        #data for clothing calculations
        self.wind = ""
        self.precip = ""
        self.current_temp_int = 0

        #data for GUI updates
        self.current_weather_time = datetime.now()
        self.current_temp_formatted = ""
        self.current_feels_like_formatted = ""
        self.weather_time_formatted = datetime.now()
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

        if "currentTemp" in formattedWeather:
            #temp and formatted temp
            self.current_temp_int = int(formattedWeather['currentTemp'])
            self.current_dew_point_int = int(formattedWeather['currentDewPoint'])
            self.current_temp_formatted = formattedWeather['currentTempFormatted']
            self.current_feels_like_formatted = formattedWeather['currentFeelsLikeFormatted']
            self.current_weather_time = datetime.strptime(formattedWeather['weatherTimeFormatted'], DATE_FORMAT)
            self.weather_time_formatted = formattedWeather['weatherTimeFormatted']

            #summary and forecast
            self.summary_text = re.sub("(.{25})", "\\1\n", formattedWeather['todaySummary'], 0, re.DOTALL)
            self.forecast_text = re.sub("(.{25})", "\\1\n", formattedWeather['tommorrowForecast'], 0, re.DOTALL)

            #weather icon
            icon_id = formattedWeather['currentIconId']
            self.weather_icon = os.path.join(DIRNAME, "../assets/" + icon_id + "@4x.png")

            #humidity/dew point icon
            self.comfort_icon = get_comfort_emoji(self.icon_config["comfort_data"], self.current_temp_int, self.current_dew_point_int, formattedWeather['currentMain'])
        else:
            #temp and formatted temp
            self.current_temp_int = 69
            self.current_dew_point_int = 69
            self.current_temp_formatted = "69°"
            self.current_weather_time = datetime.now()

            #summary and forecast
            self.summary_text = "Houston: "
            self.forecast_text = "We have a problem..."

            #weather icon
            icon_id = "high-priority.png"
            self.weather_icon = os.path.join(DIRNAME, "../assets/" + icon_id)

            #humidity/dew point icon
            self.comfort_icon = get_comfort_emoji(self.icon_config["comfort_data"], self.current_temp_int, self.current_dew_point_int, "Clear")

    def get_weather_data():

        api_config = open_config_file(API_CONFIG_FILE_NAME)
        location_config = open_config_file(LOCATION_CONFIG_FILENAME)

        weather_data = get_api_data(api_config["local_weather_endpoint"], {"lat": location_config["latitude"], "lon": location_config["longitude"]})

        return weather_data
        
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

