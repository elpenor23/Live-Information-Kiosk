from time import time
import requests
from requests.exceptions import HTTPError
import json

class WeatherManager():

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

        return json_result
    
    def get_weather_from_api(api_url, api_token, lat, lon, lang, unit, exclude):
        weather_req_url = api_url % (api_token,
                                            lat,
                                            lon,
                                            lang,
                                            unit,
                                            exclude)

        json_results = ""

        try:
            request = requests.get(weather_req_url)
            if request.status_code == 200:
                json_results = json.loads(request.text)
        except HTTPError as http_err:
            error_text = f"HTTP Error Could not get weather:{http_err}"
        except ConnectionError as http_con_err:
            error_text = f"HTTP Connection Pool Error Could not get weather:{http_con_err}"
        except json.JSONDecodeError as err:
            error_text = f'JSON Decoding error occurred: {err}'
        except Exception as err:
            error_text = f'Unknown error occurred: {err}'

        if json_results == "" or json_results is None:
            json_results = WeatherManager.create_empty_results()

        return json_results

    def get_weather_from_local_api(local_api_base, local_api_weather_endpoint, weather_api_url, api_token, lat, lon, lang, unit, exclude):
        weather_req_url = weather_api_url % (api_token,
                                            lat,
                                            lon,
                                            lang,
                                            unit,
                                            exclude)
        params = {
            'weather_api_url': weather_api_url,
            'api_token': api_token,
            'lat': lat,
            'lon': lon,
            'exclude': exclude,
            'lang': lang,
            'unit': unit
        }

        json_results = ""

        try:
            response = requests.get(local_api_base + local_api_weather_endpoint, params)
            if response.status_code == 200:
                json_results = response.json()["data"]

        except HTTPError as http_err:
            error_text = f"HTTP Error Could not get weather:{http_err}"
        except ConnectionError as http_con_err:
            error_text = f"HTTP Connection Pool Error Could not get weather:{http_con_err}"
        except json.JSONDecodeError as err:
            error_text = f'JSON Decoding error occurred: {err}'
        except Exception as err:
            error_text = f'Unknown error occurred: {err}'

        if json_results == "" or json_results is None:
            json_results = WeatherManager.create_empty_results()

        return WeatherManager.process_weather_results(json_results)

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