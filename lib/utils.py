""" Utils for getting data from api and opening config files """
import json
import os
import requests
from requests.exceptions import HTTPError

DIRNAME = os.path.dirname(__file__)
API_CONFIG_FILE_NAME = os.path.join(DIRNAME, "../config/apiConfig.json")
LOCATION_CONFIG_FILENAME = os.path.join(DIRNAME, "../config/locationConfig.json")
PEOPLE_CONFIG_FILENAME = os.path.join(DIRNAME, "../config/peopleConfig.json")
ICON_CONFIG_FILENAME = os.path.join(DIRNAME, "../config/iconConfig.json")

def open_config_file(config_filename):
    """ Opens the passed in JSON config file read only and returns it as a python dictionary"""
    try:
        with open(config_filename, 'r') as config_file:
            config_data = json.load(config_file)
    except IOError:
        error_text = "Could not read config file: " + config_filename
        print("Error: " + error_text)
    else:
        return config_data

def get_api_data(endpoint, params):
    api_config = open_config_file(API_CONFIG_FILE_NAME)
    
    results = ""
    error_text = ""

    try:
        response = requests.get(api_config["local_api_base"] + endpoint, params)
        if response.status_code == 200:
            results = response.json()
        else:
            error_text = endpoint + " API Status: " + str(response.json())
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

    if error_text != "":
        results = {"error": error_text}

    return results