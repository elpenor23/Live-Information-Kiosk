#!/usr/bin/python3
import json
import sys
import os
from lib.utils import openConfigFile
class ClothingController:
    def __init__(self, adjustedTemperature, clothingConfigFileName, gender, intensity, conditions, timeOfDay):
        #open config files
        self.clothingConfig = openConfigFile(clothingConfigFileName)
        self.gender = gender
        self.intensity = intensity
        self.conditions = conditions
        self.timeOfDay = timeOfDay
        self.adjustedTemperature = adjustedTemperature
        
        return

    def calculateItems(self):
        clothes = {}
        for bodyPart in self.clothingConfig:
            #print("--" + bodyPart + "--")
            for item in self.clothingConfig[bodyPart]:
                if item["min_temp"] <= self.adjustedTemperature <= item["max_temp"]:
                    if "gender" in item:
                        if item["gender"] == self.gender:
                            #print(item["title"] + " added with special gender!")
                            clothes[bodyPart] = item["title"]
                            break
                    elif "intensity" in item:
                        if item["intensity"].find(self.intensity) > -1:
                            # print(item["title"] + " added with special intensity!")
                            clothes[bodyPart] = item["title"]
                            break
                    elif "conditions" in item:
                        if item["conditions"].find(self.conditions) > -1:
                            #print(item["title"] + " added with special conditions!")
                            clothes[bodyPart] = item["title"]
                            break
                    elif "special" in item:
                        if item["special"] == "sunny":
                            if (self.conditions.find("clear") > -1 or self.conditions.find("partially-cloudy") > -1) and self.timeOfDay == "day":
                                # print(item["title"] + " added with special special sunny!")
                                clothes[bodyPart] = item["title"]
                                break
                        elif item["special"] == "not_rain":
                            if self.conditions.find("rain") == -1:
                                # print(item["title"] + " added with special special not_rain!")
                                clothes[bodyPart] = item["title"]
                                break
                    else:
                        # print(item["title"] + " added normally!")
                        clothes[bodyPart] = item["title"]
                        break
        
        return clothes