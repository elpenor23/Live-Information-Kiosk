""" Utils for getting data from api and opening config files """
from datetime import datetime, timedelta
from time import time
import logging
import json
import os
import requests
from requests.exceptions import HTTPError

DIRNAME = os.path.dirname(__file__)
API_CONFIG_FILE_NAME = os.path.join(DIRNAME, "../config/apiConfig.json")
LOGGER = logging.getLogger('kiosk_log')

def get_weather(lat, lon):
    """Gets the weather from the api in the apiConfig File"""

    config_data = open_config_file(API_CONFIG_FILE_NAME)
    weather_req_url = config_data["weather_req_url"]
    weather_api_token = config_data["weather_api_token"]
    weather_lang = config_data["weather_lang"]
    weather_unit = config_data["weather_unit"]
    weather_exclude_list = config_data["weather_exclude_list"]

    # get weather
    debug = False
    if debug:
        # this is here to make it easy to be sure
        # that we are hitting the api as little as possible
        # for free we only get 1000 calls a day (1 every 1.5 minutes)
        # so we do not want an error that uses them all up on us
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
        print(dt_string + " - Getting Weather From API!")

    weather_req_url = weather_req_url % (weather_api_token,
                                         lat,
                                         lon,
                                         weather_lang,
                                         weather_unit,
                                         weather_exclude_list)

    json_results = ""

    try:
        LOGGER.info("Getting Weather Data.")
        request = requests.get(weather_req_url)
        if request.status_code == 200:
            json_results = json.loads(request.text)
    except HTTPError as http_err:
        error_text = f"HTTP Error Could not get weather:{http_err}"
        LOGGER.critical(error_text)
    except ConnectionError as http_con_err:
        error_text = f"HTTP Connection Pool Error Could not get weather:{http_con_err}"
        LOGGER.critical(error_text)
    except json.JSONDecodeError as err:
        error_text = f'JSON Decoding error occurred: {err}'
        LOGGER.critical(error_text)
        json_results = create_empty_results()
    except Exception as err:
        error_text = f'Unknown error occurred: {err}'
        LOGGER.critical(error_text)

    if json_results == "" or json_results is None:
        json_results = create_empty_results()

    LOGGER.critical(json_results)
    return json_results

def create_empty_results():
    """ creates empty json string so as not to break things """
    results = {}
    results["latitude"] = 0
    results["longitude"] = 0
    results["location"] = "Error City, MI"
    results["currently"] = {}
    results['currently']['temperature'] = 69
    results['currently']['summary'] = "Error"
    results['currently']['icon'] = "fog"
    results["currently"]["windSpeed"] = 100
    results["currently"]["time"] = time()
    results["daily"] = {}
    results["daily"]["data"] = []
    results["daily"]["data"].append({})
    results["daily"]["data"][0]["summary"] = "No forecast"
    results["daily"]["summary"] = "Houston we have a problem"

    return results

def open_config_file(config_filename):
    """ Opens the passed in JSON config file read only and returns it as a python dictionary"""
    try:
        with open(config_filename, 'r') as config_file:
            config_data = json.load(config_file)
    except IOError:
        error_text = "Could not read config file: " + config_filename
        LOGGER.Error(error_text)
    else:
        return config_data

def get_indoor_status():
    config_data = open_config_file(API_CONFIG_FILE_NAME)
    status = "unknown"

    try:
        response = requests.get(config_data["indoor_req_url"] + "1")

        if response.status_code == 200:
            data = response.json()
            if data["is_set"] == 1:
                status = "inuse"
            else:
                status = "open"

            last_set = datetime.strptime(data["last_set"], "%m/%d/%Y, %H:%M:%S")
            if datetime.now() >= last_set + timedelta(minutes = 5):
                status += "-old"
    except Exception as err:
        error_text = f"Error Could not get indoor status:{err}"
        LOGGER.critical(error_text)
    finally:
        return status
