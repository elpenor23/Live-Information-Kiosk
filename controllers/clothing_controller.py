#!/usr/bin/python3
""" determines what clothing is necessary for a person and an intensity """

from lib.utils import open_config_file

class ClothingController:
    """ Calculates the clothing a person should wear"""
    def __init__(self, clothing_config_filename):
        #open config files
        self.clothing_config = open_config_file(clothing_config_filename)

        return

    def get_all_items(self):
        """ Gets all of the possible items for display """
        all_items_array = {}
        for bodyPart in self.clothing_config:
            #print("--" + bodyPart + "--")
            for item in self.clothing_config[bodyPart]:
                all_items_array[item["title"]] = item["name"]

        return all_items_array

    def calculate_items(self, adjusted_temperature, gender, intensity, conditions, time_of_day):
        """ Actually does the calculating"""
        clothes = {}
        for bodyPart in self.clothing_config:
            #print("--" + bodyPart + "--")
            for item in self.clothing_config[bodyPart]:
                if item["min_temp"] <= adjusted_temperature <= item["max_temp"]:
                    if "gender" in item:
                        if item["gender"] == gender:
                            #print(item["title"] + " added with special gender!")
                            clothes[bodyPart] = item["title"]
                            break
                    elif "intensity" in item:
                        if item["intensity"].find(intensity) > -1:
                            # print(item["title"] + " added with special intensity!")
                            clothes[bodyPart] = item["title"]
                            break
                    elif "conditions" in item:
                        if item["conditions"].find(conditions) > -1:
                            #print(item["title"] + " added with special conditions!")
                            clothes[bodyPart] = item["title"]
                            break
                    elif "special" in item:
                        if item["special"] == "sunny":
                            if (conditions.find("clear") > -1 or conditions.find("partially-cloudy") > -1) and time_of_day == "day":
                                # print(item["title"] + " added with special special sunny!")
                                clothes[bodyPart] = item["title"]
                                break
                        elif item["special"] == "not_rain":
                            if conditions.find("rain") == -1:
                                # print(item["title"] + " added with special special not_rain!")
                                clothes[bodyPart] = item["title"]
                                break
                    else:
                        # print(item["title"] + " added normally!")
                        clothes[bodyPart] = item["title"]
                        break

        return clothes
