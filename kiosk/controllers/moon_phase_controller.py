from lib.utils import open_config_file, get_api_data, API_CONFIG_FILE_NAME, LOCATION_CONFIG_FILENAME
from datetime import datetime

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATE_FORMAT_LONG = "%Y-%m-%dT%H:%M:%S%z"
TIME_FORMAT = "%-I:%M %p"
class MoonPhaseController():
    def get_moon_phase():
        api_config = open_config_file(API_CONFIG_FILE_NAME)
        location_config = open_config_file(LOCATION_CONFIG_FILENAME)

        moon_data = get_api_data(api_config["local_moon_phase_endpoint"], {"lat": location_config["latitude"], "lon": location_config["longitude"]})

        #REMOVE THIS AFTER UPDATING API: SEE BELOW
        moon_data["dayTimeFormatted"] = fortmatDayTime(moon_data)
        #END STUFF TO REMOVE

        return moon_data

#This should be moved to the API, but it was too much of a pain to update that so I added this.
#actually I am updating the API also, so if I ever install the updated API I can remove this. 
def fortmatDayTime(moon_data):
    if len(moon_data['sunriseTime']) == 19:
        formattedDayTime = datetime.strptime(moon_data['sunriseTime'], DATE_FORMAT).strftime(TIME_FORMAT) + " - " + datetime.strptime(moon_data['sunsetTime'], DATE_FORMAT).strftime(TIME_FORMAT)
    else:
        formattedDayTime = datetime.strptime(moon_data['sunriseTime'], DATE_FORMAT_LONG).strftime(TIME_FORMAT) + " - " + datetime.strptime(moon_data['sunsetTime'], DATE_FORMAT_LONG).strftime(TIME_FORMAT)

    return formattedDayTime