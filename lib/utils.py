import sys, json
import traceback
import requests
import json
import feedparser
from datetime import datetime

apiConfigFileName = "config/apiConfig.json"

def get_weather(lat, lon):
    configData = openConfigFile(apiConfigFileName)
    weather_req_url = configData["weather_req_url"]
    weather_api_token = configData["weather_api_token"]
    weather_lang = configData["weather_lang"]
    weather_unit = configData["weather_unit"]
    weather_exclude_list = configData["weather_exclude_list"]
    try:
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

        weather_req_url = weather_req_url % (weather_api_token, lat, lon, weather_lang, weather_unit, weather_exclude_list)
        r = requests.get(weather_req_url)
        return json.loads(r.text)
    except Exception as e:
        traceback.print_exc()
        errorText = "Error Could not get weather."
        print(errorText)

def openConfigFile(configFileName):
    try:
        configFile = open(configFileName, 'r')
    except IOError as ex:
        errorText = "Could not read config file: " + configFileName
        print(errorText)
        sys.exit()

    #get the data
    configData = json.loads(configFile.read())
    configFile.close
    return configData

# For Future Use. Worked at some point but not well enought to keep around
# Add these to the apiConfig.json file if you want to make this work
    # "ip_url": "http://jsonip.com/",
    # "location_req_url": "http://api.ipstack.com/%s?access_key=%s",
    # "location_api_token": "<ipstack.com token>",
    # "headlines_url": "https://news.google.com/news?ned=%s&output=rss"
# def get_ip():
#     ip_url = openConfigFile(apiConfigFileName)["ip_url"]
#     try:
#         req = requests.get(ip_url)
#         ip_json = json.loads(req.text)
#         return ip_json['ip']
#     except Exception as e:
#         traceback.print_exc()
#         errorText = "Error: Cannot get ip."
#         print(errorText)

# def get_location():
#     configData = openConfigFile(apiConfigFileName)
#     location_req_url = configData["location_req_url"]
#     location_api_token = configData["location_api_token"]
#     try:
#         # get location
#         location_req_url = location_req_url % (get_ip(), location_api_token)
#         r = requests.get(location_req_url)
#         location_obj = json.loads(r.text)
      
#         return_data  = {}
#         return_data['lat'] = location_obj['latitude']
#         return_data['lon'] = location_obj['longitude']
#         return_data['location'] = "%s, %s" % (location_obj['city'], location_obj['region_code'])
        
#         return return_data
#     except Exception as e:
#         traceback.print_exc()
#         errorText = "Error Could not get location."
#         print(errorText)
        
# def get_news(news_country_code):
#     configData = openConfigFile(apiConfigFileName)
#     headlines_url = configData["headlines_url"]
#     try:
#         if news_country_code == None: news_country_code = "us"

#         headlines_url = headlines_url % news_country_code

#         return feedparser.parse(headlines_url)
#     except Exception as e:
#         traceback.print_exc()
#         errorText = "Error Could not get news."
#         print(errorText)