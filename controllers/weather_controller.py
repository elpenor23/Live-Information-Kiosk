#!/usr/bin/python3
"""
parses the weather data from the api
and makes it available to the weather frame
"""
import os
from lib.utils import get_weather, open_config_file

# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter
DIRNAME = os.path.dirname(__file__)

ICON_LOOKUP = {
    'clear-day': os.path.join(DIRNAME, "../assets/Sun.png"),  # clear sky day
    'wind': os.path.join(DIRNAME, "../assets/Wind.png"),   #wind
    'cloudy': os.path.join(DIRNAME, "../assets/Cloud.png"),  # cloudy day
    'partly-cloudy-day': os.path.join(DIRNAME, "../assets/PartlySunny.png"),  # partly cloudy day
    'rain': os.path.join(DIRNAME, "../assets/Rain.png"),  # rain day
    'snow': os.path.join(DIRNAME, "../assets/Snow.png"),  # snow day
    'snow-thin': os.path.join(DIRNAME, "../assets/Snow.png"),  # sleet day
    'fog': os.path.join(DIRNAME, "../assets/Haze.png"),  # fog day
    'clear-night': os.path.join(DIRNAME, "../assets/Moon.png"),  # clear sky night
    'partly-cloudy-night': os.path.join(DIRNAME, "../assets/PartlyMoon.png"),  # partly cloudy night
    'thunderstorm': os.path.join(DIRNAME, "../assets/Storm.png"),  # thunderstorm
    'tornado': os.path.join(DIRNAME, "../assests/Tornado.png"),    # tornado
    'hail': os.path.join(DIRNAME, "../assests/Hail.png")  # hail
}

class WeatherController(object):
    """ Parses the weather data for the frame """
    def __init__(self, weather_config):
        """ initializes all of the weather data """
        #data for clothing calculations
        self.wind = ""
        self.time_of_day = ""
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
        latitude = self.weather_config["latitude"]
        longitude = self.weather_config["longitude"]
        location = self.weather_config["location"]

        self.location = location

        self.weather_obj = get_weather(latitude, longitude)

        #temp and formatted temp
        degree_sign = u'\N{DEGREE SIGN}'
        self.current_temp_int = int(self.weather_obj['currently']['temperature'])
        self.current_temp_formatted = "%s%s" % (str(self.current_temp_int), degree_sign)

        #summary and forecast
        self.summary_text = self.weather_obj['currently']['summary']
        self.forecast_text = self.weather_obj["daily"]["data"][0]["summary"] + "\n" + self.weather_obj["daily"]["summary"]

        #weather icon
        icon_id = self.weather_obj['currently']['icon']
        if icon_id in ICON_LOOKUP:
            self.weather_icon = ICON_LOOKUP[icon_id]

        self.time_of_day = icon_id

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        """
        Static method for
        converting degrees kelvin to degrees fahrenheit
        """
        return 1.8 * (kelvin_temp - 273) + 32
