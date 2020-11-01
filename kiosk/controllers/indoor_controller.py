from lib.utils import API_CONFIG_FILE_NAME, open_config_file
from datetime import datetime, timedelta
from obj.enums import Indoor_Status, Light_Status
from lib.utils import API_CONFIG_FILE_NAME, get_api_data

DATA_EXPIRES_TIME = 5

class IndoorController():
    def __init__(self):
        self.config_data = open_config_file(API_CONFIG_FILE_NAME)
        self.dataHasExpired = False
        self.Indoor_Status = Indoor_Status.UNKNOWN
        self.Light_Status = Light_Status.UNKNOWN
        self.update_statuses()

    def update_statuses(self):       
        # if we do not have an indoor we need to return None and hide all the things
        if self.config_data["local_indoor_status_endpoint"] == "None":
            self.Indoor_Status = Indoor_Status.NONE

        data = get_api_data(self.config_data["local_indoor_status_endpoint"], {})

        status_data = data["data"]
        last_set = datetime.strptime(data["last_set"], "%m/%d/%Y, %H:%M:%S")
        self.process_indoor_info(status_data)
        self.dataHasExpired = datetime.now() >= last_set + timedelta(minutes = DATA_EXPIRES_TIME)


    def process_indoor_info(self, data):
        status = Indoor_Status.FREE
 
        if data.find("B") > -1 and data.find("W") > -1:
            status = Indoor_Status.WIFIANDBLUETOOTH
        else:
            if data.find("B") > -1:
                status = Indoor_Status.BLUETOOTH
            
            if data.find("W") > -1:
                status = Indoor_Status.WIFI
        
        self.Indoor_Status = status

        if data.find("L") > -1:
            self.Light_Status = Light_Status.ON
        else:
            self.Light_Status = Light_Status.OFF
