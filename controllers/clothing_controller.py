#!/usr/bin/python3
""" determines what clothing is necessary for a person and an intensity """

from lib.utils import open_config_file

class ClothingController:
    """ Calculates the clothing a person should wear"""
    def __init__(self, adjusted_temperature, clothing_config_filename, gender, intensity, conditions, time_of_day):
        #open config files
        self.clothing_config = open_config_file(clothing_config_filename)
        self.gender = gender
        self.intensity = intensity
        self.conditions = conditions
        self.time_of_day = time_of_day
        self.adjusted_temperature = adjusted_temperature

        return

    def calculate_items(self):
        """ Actually does the calculating"""
        clothes = {}
        for bodyPart in self.clothing_config:
            #print("--" + bodyPart + "--")
            for item in self.clothing_config[bodyPart]:
                if item["min_temp"] <= self.adjusted_temperature <= item["max_temp"]:
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
                            if (self.conditions.find("clear") > -1 or self.conditions.find("partially-cloudy") > -1) and self.time_of_day == "day":
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
