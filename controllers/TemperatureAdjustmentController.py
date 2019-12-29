#!/usr/bin/python3
import json
import sys
import os

class TemperatureAdjustmentController:
    def __init__(self, timeOfDay, precip, wind, gender, feel, intensity, currentTemp, tempAdjustConfig):
        self.wind = wind
        self.timeOfDay = timeOfDay
        self.precip = precip
        self.gender = gender
        self.intensity = intensity
        self.feel = feel
        self.currentTemp = currentTemp

        #open config files
        self.tempAdjustmentConfig = tempAdjustConfig 
        self.adjustedTemperature = self.get_adjustedTemperature()
        return

    def get_adjustedTemperature(self):
        tempAdjustmentTimeOfDayAndConditions = 0
        #time of day and conditions
        if self.timeOfDay == "day" and self.precip.startswith("clear"):
            tempAdjustmentTimeOfDayAndConditions += self.tempAdjustmentConfig["timeofday_precipitation"]["clear_day"]
        elif self.timeOfDay == "day" and self.precip.startswith("partly_cloudy"):
            tempAdjustmentTimeOfDayAndConditions += self.tempAdjustmentConfig["timeofday_precipitation"]["partially_cloudy_day"]
        elif (self.timeOfDay == "dawn" or self.timeOfDay == "dusk") and self.precip.startswith("clear"):
            tempAdjustmentTimeOfDayAndConditions += self.tempAdjustmentConfig["timeofday_precipitation"]["clear_dusk_dawn"]
        elif (self.timeOfDay == "dawn" or self.timeOfDay == "dusk") and self.precip.startswith("partly_cloudly"):
            tempAdjustmentTimeOfDayAndConditions += self.tempAdjustmentConfig["timeofday_precipitation"]["partially_cloudy_dusk_dawn"]
        elif self.precip == "rain":
            tempAdjustmentTimeOfDayAndConditions += self.tempAdjustmentConfig["timeofday_precipitation"]["rain"]
        elif self.precip == "light_rain":
            tempAdjustmentTimeOfDayAndConditions += self.tempAdjustmentConfig["timeofday_precipitation"]["light_rain"]
        elif self.precip == "snow":
            tempAdjustmentTimeOfDayAndConditions += self.tempAdjustmentConfig["timeofday_precipitation"]["snow"]

        tempAdjustmentWind = 0
        #wind
        if self.wind == "light_wind":
            tempAdjustmentWind += self.tempAdjustmentConfig["wind"]["light_wind"]
        elif self.wind == "windy":
            tempAdjustmentWind += self.tempAdjustmentConfig["wind"]["windy"]
        elif self.wind == "heavy_wind":
            tempAdjustmentWind += self.tempAdjustmentConfig["wind"]["heavy_wind"]

        tempAdjustmentIntensity = 0
        #intensity
        if self.intensity == "race":
            tempAdjustmentIntensity += self.tempAdjustmentConfig["intensity"]["race"]
        elif self.intensity == "hard_workout":
            tempAdjustmentIntensity += self.tempAdjustmentConfig["intensity"]["hard_workout"]
        elif self.intensity == "long_run":
            tempAdjustmentIntensity += self.tempAdjustmentConfig["intensity"]["long_run"]

        tempAdjustmentFeel = 0
        #feel
        if self.feel == "cool":
            tempAdjustmentFeel += self.tempAdjustmentConfig["feel"]["cool"]
        elif self.feel == "warm":
            tempAdjustmentFeel += self.tempAdjustmentConfig["feel"]["warm"]

        tempAdjustmentGender = 0
        #gender
        if self.gender == "man":
            tempAdjustmentGender += self.tempAdjustmentConfig["gender"]["man"]
        elif self.gender == "woman":
            tempAdjustmentGender += self.tempAdjustmentConfig["gender"]["woman"]

        finalAdjustedTemp = self.currentTemp + tempAdjustmentTimeOfDayAndConditions + tempAdjustmentWind + tempAdjustmentIntensity + tempAdjustmentFeel + tempAdjustmentGender

        debug = False
        if debug:
            print("Real Temp: " + str(self.currentTemp))
            print("TimeofDay and Conditions Adjust(" + self.timeOfDay + ", " + self.precip + "): " + str(tempAdjustmentTimeOfDayAndConditions))
            print("Wind Adjust: " + str(tempAdjustmentWind))
            print("Intensity Adjust: " + str(tempAdjustmentIntensity))
            print("Feel Adjust: " + str(tempAdjustmentFeel))
            print("Gender Adjust: " + str(tempAdjustmentGender))

        return finalAdjustedTemp
    
    #adjustedTemperature = property(get_adjustedTemperature)

    def get_headwear(self):
        return ""
    
    headwear = property(get_headwear)