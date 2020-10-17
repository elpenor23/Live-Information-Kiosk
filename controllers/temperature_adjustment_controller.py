#!/usr/bin/python3
""" Adjusts the temp based on all the things """
import logging
from lib.utils import open_config_file

class TemperatureAdjustmentController:
    """ Adjusts the temp based on things"""
    def __init__(self, 
                 time_of_day,
                 precip,
                 wind_speed,
                 gender,
                 feel,
                 intensity,
                 current_temp,
                 temp_adjust_config_filename):
        
        self.temp_adjust_config = open_config_file(temp_adjust_config_filename)

        self.logger = logging.getLogger('kiosk_log')
        self.wind  = self.get_wind(wind_speed,
                        self.temp_adjust_config["wind_speed"])
        self.time_of_day = time_of_day
        self.precip = precip
        self.gender = gender
        self.intensity = intensity
        self.feel = feel
        self.current_temp = current_temp

        self.adjusted_temperature = self.get_adjusted_temperature()
        return

    def get_adjusted_temperature(self):
        """ gets the adjusted temp"""
        temp_adjustment_time_of_day_and_conditions = 0
        #time of day and conditions
        if self.time_of_day == "day" and self.precip == "Clear":
            temp_adjustment_time_of_day_and_conditions += (
                self.temp_adjust_config["timeofday_precipitation"]["clear_day"])

        elif self.time_of_day == "day" and (self.precip == "Clouds" or self.precip == "Mist"):
            temp_adjustment_time_of_day_and_conditions += (
                self.temp_adjust_config["timeofday_precipitation"]["partially_cloudy_day"])

        elif ((self.time_of_day == "dawn" or self.time_of_day == "dusk") and self.precip == "Clear"):
            temp_adjustment_time_of_day_and_conditions += (
                self.temp_adjust_config["timeofday_precipitation"]["clear_dusk_dawn"])

        elif ((self.time_of_day == "dawn" or self.time_of_day == "dusk") and (self.precip == "Clouds" or self.precip == "Mist")):
            temp_adjustment_time_of_day_and_conditions += (
                self.temp_adjust_config["timeofday_precipitation"]["partially_cloudy_dusk_dawn"])

        elif self.precip == "Rain":
            temp_adjustment_time_of_day_and_conditions += (
                self.temp_adjust_config["timeofday_precipitation"]["rain"])

        elif self.precip == "Drizzle":
            temp_adjustment_time_of_day_and_conditions += (
                self.temp_adjust_config["timeofday_precipitation"]["light_rain"])

        elif self.precip == "Snow":
            temp_adjustment_time_of_day_and_conditions += (
                self.temp_adjust_config["timeofday_precipitation"]["snow"])

        temp_adjustment_wind = 0
        #wind
        if self.wind == "light_wind":
            temp_adjustment_wind += self.temp_adjust_config["wind"]["light_wind"]
        elif self.wind == "windy":
            temp_adjustment_wind += self.temp_adjust_config["wind"]["windy"]
        elif self.wind == "heavy_wind":
            temp_adjustment_wind += self.temp_adjust_config["wind"]["heavy_wind"]

        temp_adjustment_intensity = 0
        #intensity
        if self.intensity == "race":
            temp_adjustment_intensity += self.temp_adjust_config["intensity"]["race"]
        elif self.intensity == "hard_workout":
            temp_adjustment_intensity += self.temp_adjust_config["intensity"]["hard_workout"]
        elif self.intensity == "long_run":
            temp_adjustment_intensity += self.temp_adjust_config["intensity"]["long_run"]

        temp_adjustment_feel = 0
        #feel
        if self.feel == "cool":
            temp_adjustment_feel += self.temp_adjust_config["feel"]["cool"]
        elif self.feel == "warm":
            temp_adjustment_feel += self.temp_adjust_config["feel"]["warm"]

        temp_adjustment_gender = 0
        #gender
        if self.gender == "man":
            temp_adjustment_gender += self.temp_adjust_config["gender"]["man"]
        elif self.gender == "woman":
            temp_adjustment_gender += self.temp_adjust_config["gender"]["woman"]

        final_adjusted_temp = (self.current_temp +
                               temp_adjustment_time_of_day_and_conditions +
                               temp_adjustment_wind +
                               temp_adjustment_intensity +
                               temp_adjustment_feel +
                               temp_adjustment_gender)


        self.logger.debug("Real Temp: " + str(self.current_temp))
        self.logger.debug("TimeofDay and Conditions Adjust(" +
                self.time_of_day + ", " + self.precip +
                "): " + str(temp_adjustment_time_of_day_and_conditions))
        self.logger.debug("Wind Adjust (" + self.wind + "): " + str(temp_adjustment_wind))
        self.logger.debug("Intensity Adjust (" + self.intensity + "): " + str(temp_adjustment_intensity))
        self.logger.debug("Feel Adjust (" + self.feel + "): " + str(temp_adjustment_feel))
        self.logger.debug("Gender Adjust (" + self.gender + "): " + str(temp_adjustment_gender))

        return final_adjusted_temp

    def get_wind(self, wind_speed, wind_speed_config):
        """
        Take the wind speed and calculate the wind type
        """
        return_value = "None"
        if wind_speed_config["light_min"] <= wind_speed <= wind_speed_config["light_max"]:
            return_value = "light_wind"
        elif wind_speed_config["wind_min"] <= wind_speed <= wind_speed_config["wind_max"]:
            return_value = "windy"
        elif wind_speed_config["heavy_min"] <= wind_speed <= wind_speed_config["heavy_max"]:
            return_value = "heavy_wind"

        return return_value