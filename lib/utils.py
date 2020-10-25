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
LOCATION_CONFIG_FILENAME = os.path.join(DIRNAME, "../config/locationConfig.json")
PEOPLE_CONFIG_FILENAME = os.path.join(DIRNAME, "../config/peopleConfig.json")
TEMP_ADJUSTMENT_CONFIG_FILENAME = os.path.join(DIRNAME, "../config/tempAdjustConfig.json")

LOGGER = logging.getLogger('kiosk_log')

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
