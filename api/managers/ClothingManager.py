from managers.TemperatureAdjustmentManager import TemperatureAdjustmentManager
from managers.WeatherManager import WeatherManager
from managers.ConfigManager import ConfigManager
from enums.Enums import WeatherFetch
from lib.sunrise import Sun
from datetime import datetime, timezone

class ClothingManager():
    def get_bodyparts():
        # returns list of body parts that have clothing associated
        data = {}
        ary = []
        clothingConfig = ConfigManager.get_clothing_config_data()
        if "error" not in clothingConfig:
            for bodypart in clothingConfig:
                ary.append( bodypart)

            data["data"] = ary

            return data

        return {"error": "Error getting bodyparts"}, 500

    def get_all_clothing_for_bodypart(bodypart):
        #returns all clothing available for a single bodypart
        return{}

    def get_all_clothing():
        # read config and return clothing titles
        # UI can use this to build stuff if it needs it
        clothingConfig = ConfigManager.get_clothing_config_data()
        if "error" not in clothingConfig:
            data = {}
            info = {}
            for bodypart in clothingConfig:
                
                for clothing in clothingConfig[bodypart]:
                    info[clothing["name"]] = {}
                    info[clothing["name"]]["bodypart"] = bodypart
                    info[clothing["name"]]["title"] = clothing["title"]

            data["data"] = info

            return data
        return {"error": "Error getting all clothing"}, 500

    def calculate_clothing(ids_csv, feels_csv, gender_csv, name_csv, color_csv, lat, lon):
        # takes in a person list and returns a 
        # dict of clothing for each person
        id_array = ids_csv.split(',')
        feel_ary = feels_csv.split(',')
        gender_ary = gender_csv.split(',')
        name_ary = name_csv.split(',')
        color_ary = color_csv.split(',')

        if len(feel_ary) != len(gender_ary) != len(name_ary) != len(color_ary) != len(id_array):
            # status HTTP_400_BAD_REQUEST 
            return {"message": "people values do not match"}, 400 

        #setup the people objects to loop through
        people = create_people(id_array, feel_ary, gender_ary, name_ary, color_ary)

        #get weather and time of day
        weather = WeatherManager.get_weather(WeatherFetch.NORMAL, lat, lon)
        if "error" not in weather:
            time_of_day = get_time_of_day(weather["weather_time"], lat, lon)

            #get intensities
            intensity_data = ConfigManager.get_intensity_config_data()

            results = calculate(people, intensity_data, weather, time_of_day)

            return results
        else:
            return weather, 500 #weather just holds the error at this point not the actual weather

def calculate(people, intensities, weather, time_of_day):
    results = []

    for person in people["people"]:
        temp_person = {}
        temp_person["id"] = person["id"]
        temp_person["gender"] = person["gender"]
        temp_person["feel"] = person["feel"]
        temp_person["name"] = person["name"]
        temp_person["color"] = person["color"]
        temp_person["data"] = []
        for intensity in intensities["intensities"]:
            temp = {}

            adjusted_temp = TemperatureAdjustmentManager.get_adjusted_temperature(time_of_day, weather["current_main"], weather["current_wind_speed"], person["feel"], intensity["type"], weather["current_temp_int"])
            clothes = calculate_items( adjusted_temp, person["gender"], intensity, weather["current_main"], time_of_day)
            temp["intensity"] = intensity["name"]
            temp["intensity_type"] = intensity["type"]
            temp["clothes"] = clothes
            temp_person["data"].append(temp)

        results.append(temp_person)

    return results

def get_time_of_day(t, lat, lon):
    weather_time = datetime.fromtimestamp(t)
    weather_time = weather_time.replace(tzinfo=timezone.utc)

    sunrise_sunset = Sun(lat=float(lat),
                        long=float(lon))
    return sunrise_sunset.time_of_day(weather_time)


def create_people(ids_ary, feel_ary, gender_ary, name_ary, color_ary):
    people = {}
    people["people"] = []
    for i in range (len(feel_ary)):
        person = {}
        person["id"] = ids_ary[i]
        person["feel"] = feel_ary[i]
        person["gender"] = gender_ary[i]
        person["name"] = name_ary[i]
        person["color"] = color_ary[i]
        people["people"].append(person)

    return people

def calculate_items(adjusted_temperature, gender, intensity, conditions, time_of_day):
    """ Actually does the calculating"""
    clothing_config = ConfigManager.get_clothing_config_data()
    clothes = {}
    for bodyPart in clothing_config:
        #print("--" + bodyPart + "--")
        for item in clothing_config[bodyPart]:
            if item["min_temp"] <= adjusted_temperature <= item["max_temp"]:
                if "gender" in item:
                    if item["gender"] == gender:
                        #print(item["title"] + " added with special gender!")
                        clothes[bodyPart] = item["title"]
                        clothes[bodyPart + "_name"] = item["name"]
                        break
                elif "intensity" in item:
                    if item["intensity"].find(intensity) > -1:
                        # print(item["title"] + " added with special intensity!")
                        clothes[bodyPart] = item["title"]
                        clothes[bodyPart + "_name"] = item["name"]
                        break
                elif "conditions" in item:
                    if item["conditions"].find(conditions) > -1:
                        #print(item["title"] + " added with special conditions!")
                        clothes[bodyPart] = item["title"]
                        clothes[bodyPart + "_name"] = item["name"]
                        break
                elif "special" in item:
                    if item["special"] == "sunny":
                        if conditions.find("Clear") > -1 and time_of_day == "day":
                            # print(item["title"] + " added with special special sunny!")
                            clothes[bodyPart] = item["title"]
                            clothes[bodyPart + "_name"] = item["name"]
                            break
                    elif item["special"] == "not_rain":
                        if conditions.find("Rain") == -1:
                            # print(item["title"] + " added with special special not_rain!")
                            clothes[bodyPart] = item["title"]
                            clothes[bodyPart + "_name"] = item["name"]
                            break
                    elif item["special"] == "singlet":
                        if intensity == "race":
                            clothes[bodyPart] = item["title"]
                            clothes[bodyPart + "_name"] = item["name"]
                            break
                else:
                    # print(item["title"] + " added normally!")
                    clothes[bodyPart] = item["title"]
                    clothes[bodyPart + "_name"] = item["name"]
                    break

    return clothes
