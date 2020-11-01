from lib.utils import open_config_file, get_api_data, API_CONFIG_FILE_NAME

class MoonPhaseController():
    def get_moon_phase():
        api_config = open_config_file(API_CONFIG_FILE_NAME)

        moon_data = get_api_data(api_config["local_moon_phase_endpoint"], {})

        return moon_data