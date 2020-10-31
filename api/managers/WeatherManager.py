from time import time
from datetime import datetime, timedelta
import requests
from requests.exceptions import HTTPError
import json
from database.database import db
from database.WeatherModel import WeatherModel
from managers.ConfigManager import ConfigManager
from enums.Enums import WeatherFetch


class WeatherManager():

    def setup_db():
        new_status = WeatherModel(data = json.dumps(create_empty_results()), last_set = (datetime.now() - timedelta(minutes = 60)))
        db.session.add(new_status)
        db.session.commit()

    def get_weather(fetchType, lat, lon):
        """Gets the weather from the api in the apiConfig File"""
        # get weather
        allWeatherResults = WeatherModel.query.all()
        db_weather = allWeatherResults[0]
        current_time = datetime.now()

        #should we use the local data or refresh it?
        if fetchType == WeatherFetch.FORCEREFRESH or (fetchType == WeatherFetch.NORMAL and db_weather.last_set <= (current_time - timedelta(minutes = 1))):
            #get the weather from the api and save it locally
            fromCache = False
            weather = get_weather_from_api(lat, lon)
            db_weather.data = json.dumps(weather)
            db_weather.last_set = current_time
            db.session.commit()
        else:
            #return weather we already have
            fromCache = True
            weather = json.loads(db_weather.data)

        processed_results = process_weather_results(weather)
        
        if fromCache:
            processed_results["type"] = "cached"
        else:
            processed_results["type"] = "refreshed"

        return processed_results

#
# Local functions used by the manager
#
def process_weather_results(raw_json_results):
    json_result = {}
    degree_sign = u'\N{DEGREE SIGN}'

    json_result["lat"] =  raw_json_results['lat']
    json_result["lon"] =  raw_json_results['lon']

    json_result["current_temp_int"] =  int(raw_json_results['current']['temp'])

    json_result["current_dew_point_int"] = int(raw_json_results['current']['dew_point'])

    #format temps for display
    json_result["current_temp_formatted"] = "%s%s " % (str(json_result["current_temp_int"]), degree_sign)
    json_result["min_temp"] = "%s%s" % (str(int(raw_json_results["daily"][0]["temp"]["min"])), degree_sign)
    json_result["max_temp"] = "%s%s" % (str(int(raw_json_results["daily"][0]["temp"]["max"])), degree_sign)

    #summary and forecast
    json_result["summary_text"] = ("Today: " + raw_json_results['current']['weather'][0]["description"] + "\n" + 
                        "Low: " + json_result["min_temp"] + " / High: " + json_result["max_temp"])

    min_temp = "%s%s" % (str(int(raw_json_results["daily"][1]["temp"]["min"])), degree_sign)
    max_temp = "%s%s" % (str(int(raw_json_results["daily"][1]["temp"]["max"])), degree_sign)

    json_result["forecast_text"] = ("Tomorrow: " + raw_json_results["daily"][1]["weather"][0]["description"] + 
                            "\nLow: " + min_temp + " / High: " + max_temp)

    json_result["icon_id"] = raw_json_results['current']["weather"][0]['icon']

    json_result["current_main"] = raw_json_results['current']['weather'][0]["main"]

    json_result["weather_time"] = raw_json_results["current"]["dt"]

    json_result["current_wind_speed"] = raw_json_results["current"]["wind_speed"]

    json_result["error"] = raw_json_results["error"]

    return json_result


def get_weather_from_api(lat, lon):
    json_results = ""
    error_text = ""
    
    apiConfig = ConfigManager.get_api_config_data()

    if not "error" in apiConfig:

        try:
            weather_req_url = apiConfig["weather_req_url"] % (apiConfig["weather_api_token"],
                                                            lat,
                                                            lon,
                                                            apiConfig["weather_lang"],
                                                            apiConfig["weather_unit"],
                                                            apiConfig["weather_exclude_list"])

            request = requests.get(weather_req_url)
            if request.status_code == 200:
                json_results = json.loads(request.text)
            else:
                error_text = "Weather API Status: " + str(request.json())
        except HTTPError as http_err:
            error_text = f"HTTP Error Could not get weather:{http_err}"
        except ConnectionError as http_con_err:
            error_text = f"HTTP Connection Pool Error Could not get weather:{http_con_err}"
        except json.JSONDecodeError as err:
            error_text = f'JSON Decoding error occurred: {err}'
        except KeyError as key_err:
            error_text = f'JSON key error occurred: {key_err}'
        except Exception as err:
            error_text = f'Unknown error occurred: {err}'
    else:
        error_text = apiConfig["error"]

    if json_results == "" or json_results is None:
        json_results = create_empty_results()

    json_results["error"] = error_text

    return json_results

def create_empty_results():
    """ creates empty json string so as not to break things """
    results = {}
    results["lat"] = 0
    results["lon"] = 0
    results["location"] = "Error City, MI"
    results["current"] = {}
    results['current']['temp'] = 69
    results['current']['dew_point'] = 69
    results['current']["weather"] = [{}]
    results['current']["weather"][0]['main'] = "Tornado"
    results['current']["weather"][0]['description'] = "Houston we have a problem!"
    results['current']["weather"][0]['icon'] = "50d"
    results["current"]["wind_speed"] = 100
    results["current"]["dt"] = time()
    results["daily"] = [{}, {}]

    results["daily"][0]["temp"] = {}
    results["daily"][0]["temp"]["min"] = -100
    results["daily"][0]["temp"]["max"] = 100
    results["daily"][0]["weather"] = [{}]
    results["daily"][0]["weather"][0]["main"] = "Tornado"
    results["daily"][0]["weather"][0]["description"] = "Houston we have a problem!"

    results["daily"][1]["temp"] = {}
    results["daily"][1]["temp"]["min"] = -100
    results["daily"][1]["temp"]["max"] = 100
    results["daily"][1]["weather"] = [{}]
    results["daily"][1]["weather"][0]["main"] = "Tornado"
    results["daily"][1]["weather"][0]["description"] = "Houston We have a problem!"

    return results