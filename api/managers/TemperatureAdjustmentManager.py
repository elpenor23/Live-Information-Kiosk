#!/usr/bin/python3
""" Adjusts the temp based on all the things """

from managers.ConfigManager import ConfigManager

class TemperatureAdjustmentManager:
    """ Adjusts the temp based on things"""
    def get_adjusted_temperature(time_of_day, precip, wind_speed, feel, intensity, current_temp):
        """ gets the adjusted temp"""
        temp_adjust_config = ConfigManager.get_temperature_adjustment_config_data()
        
        temp_adjustment_time_of_day_and_conditions = 0
        #time of day and conditions
        if time_of_day == "day" and precip == "Clear":
            temp_adjustment_time_of_day_and_conditions += (
                temp_adjust_config["timeofday_precipitation"]["clear_day"])

        elif time_of_day == "day" and (precip == "Clouds" or precip == "Mist"):
            temp_adjustment_time_of_day_and_conditions += (
                temp_adjust_config["timeofday_precipitation"]["partially_cloudy_day"])

        elif ((time_of_day == "dawn" or time_of_day == "dusk") and precip == "Clear"):
            temp_adjustment_time_of_day_and_conditions += (
                temp_adjust_config["timeofday_precipitation"]["clear_dusk_dawn"])

        elif ((time_of_day == "dawn" or time_of_day == "dusk") and (precip == "Clouds" or precip == "Mist")):
            temp_adjustment_time_of_day_and_conditions += (
                temp_adjust_config["timeofday_precipitation"]["partially_cloudy_dusk_dawn"])

        elif precip == "Rain":
            temp_adjustment_time_of_day_and_conditions += (
                temp_adjust_config["timeofday_precipitation"]["rain"])

        elif precip == "Drizzle":
            temp_adjustment_time_of_day_and_conditions += (
                temp_adjust_config["timeofday_precipitation"]["light_rain"])

        elif precip == "Snow":
            temp_adjustment_time_of_day_and_conditions += (
                temp_adjust_config["timeofday_precipitation"]["snow"])

        temp_adjustment_wind = 0
        wind  = get_wind(wind_speed, temp_adjust_config["wind_speed"])
        #wind
        if wind == "light_wind":
            temp_adjustment_wind += temp_adjust_config["wind"]["light_wind"]
        elif wind == "windy":
            temp_adjustment_wind += temp_adjust_config["wind"]["windy"]
        elif wind == "heavy_wind":
            temp_adjustment_wind += temp_adjust_config["wind"]["heavy_wind"]

        temp_adjustment_intensity = 0
        #intensity
        if intensity == "race":
            temp_adjustment_intensity += temp_adjust_config["intensity"]["race"]
        elif intensity == "hard_workout":
            temp_adjustment_intensity += temp_adjust_config["intensity"]["hard_workout"]
        elif intensity == "long_run":
            temp_adjustment_intensity += temp_adjust_config["intensity"]["long_run"]

        temp_adjustment_feel = 0
        #feel
        if feel == "cool":
            temp_adjustment_feel += temp_adjust_config["feel"]["cool"]
        elif feel == "warm":
            temp_adjustment_feel += temp_adjust_config["feel"]["warm"]

        final_adjusted_temp = (current_temp +
                                temp_adjustment_time_of_day_and_conditions +
                                temp_adjustment_wind +
                                temp_adjustment_intensity +
                                temp_adjustment_feel)

        return final_adjusted_temp

def get_wind(wind_speed, wind_speed_config):
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