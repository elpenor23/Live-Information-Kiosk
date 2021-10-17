""" Utils for getting data from api and opening config files """
import json
import os
import requests
import logging
from logging.handlers import RotatingFileHandler
from requests.exceptions import HTTPError

DIRNAME = os.path.dirname(__file__)
LOG_FILENAME = os.path.join(DIRNAME, "../log/error.log")
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
        error_log = get_logger()
        error_log.critical("Error opening config file: " + config_filename + " - " + error_text)
    else:
        return config_data

def get_api_data(endpoint, params):
    api_config = open_config_file(API_CONFIG_FILE_NAME)
    
    results = {}
    error_text = ""
    responce_error_text = ""

    try:
        response = requests.get(api_config["local_api_base"] + endpoint, params)
        results = response.json()
        if response.status_code != 200:
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

    if "error" in results:
        responce_error_text = results["error"]

    if responce_error_text != "" or error_text != "":
        log_error("Endpoint: " + endpoint + " | params: " + str(params) + " | API Error: " + error_text + " | Response Error: " + responce_error_text)

    return results

def get_logger():
    """ Initializes the logger for the entire program """
    # Set up a specific logger with our desired output level
    logger = logging.getLogger("kiosk_error_log")
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(LOG_FILENAME, maxBytes=100000, backupCount=10)
    logger.addHandler(handler)
    log_formatter = logging.Formatter('{asctime}: {levelname:8s} - {message}', style='{')
    handler.setFormatter(log_formatter)

    return logger

def log_error(message):
        # logger = get_logger()
        # logger.critical(message)
        print(message)