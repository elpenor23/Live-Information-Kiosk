""" Utils for getting data from api and opening config files """
import json
import os
import requests
import logging
from logging.handlers import RotatingFileHandler
from requests.exceptions import HTTPError
from datetime import datetime

DIRNAME = os.path.dirname(__file__)
LOG_FILENAME = os.path.join(DIRNAME, "../log/error.log")
API_CONFIG_FILE_NAME = os.path.join(DIRNAME, "../config/apiConfig.json")
LOCATION_CONFIG_FILENAME = os.path.join(DIRNAME, "../config/locationConfig.json")
PEOPLE_CONFIG_FILENAME = os.path.join(DIRNAME, "../config/peopleConfig.json")
ICON_CONFIG_FILENAME = os.path.join(DIRNAME, "../config/iconConfig.json")
THREAD_CONFIG_FILENAME = os.path.join(DIRNAME, "../config/threadConfig.json")

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
        uri = api_config["local_api_base"] + endpoint
        response = requests.get(uri, params)
        
        if response.status_code != 200:
            error_text = endpoint + "\n API Status: " + str(response)
        else:
            results = response.json()
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
        log_error("ERROR(" + datetime.now().strftime("%Y%m%dT%H:%M:%S") + "):\nEndpoint: " + endpoint + " \nparams: " + str(params) + " \nAPI Error: " + error_text + " \nResponse Error: " + responce_error_text + "\n")

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

def format_summary_text(summary_text,max_length):
    sum_lst = summary_text.split()
    summary = ""
    sum_part = ""
    
    for i in sum_lst:
        # we want the Low and high to be on their own line
        # so we need to reset things when Low shows up.
        # but then continue normally
        if i.startswith("Low:"):
            summary += sum_part + "\n"
            sum_part = ""
            
        sum_part += i + " "
        if len(sum_part) >= max_length:
            summary += sum_part + "\n"
            sum_part = ""
    
    if sum_part != "":  # add the last part of the summary if it's not empty
        summary += sum_part.strip() + "\n"
    
    # summary = summary.replace("Low:", "\nLow:")
        
    return summary.strip()
    