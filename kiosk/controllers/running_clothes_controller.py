from lib.utils import open_config_file, get_api_data, PEOPLE_CONFIG_FILENAME, LOCATION_CONFIG_FILENAME
CLOTHING_API_ENDPOINT = "Clothing"
CALCULATE_API_ENDPOINT = CLOTHING_API_ENDPOINT + "/Calculate"

class RunningClothesController():
    
    def get_runner_data():
        people = open_config_file(PEOPLE_CONFIG_FILENAME)
        location = open_config_file(LOCATION_CONFIG_FILENAME)
        
        #parms
        names = ""
        feels = ""
        colors = ""
        ids = ""
        
        #setup parms
        for person in people["people"]:
            if ids != "":
                ids += ','
            ids += str(person["id"])

            if names != "":
                names += ','
            names += person["name"]

            if feels != "":
                feels += ','
            feels += person["feel"]

            if colors != "":
                colors += ','
            colors += person["color"]

        params = {
            "lat": location["latitude"],
            "lon": location["longitude"],
            "ids": ids,
            "feels": feels,
            "names": names,
            "colors": colors
        }

        results = get_api_data(CALCULATE_API_ENDPOINT, params)

        return results

    def get_all_items():
        params = {}
        all_items = get_api_data(CLOTHING_API_ENDPOINT, params)
        return all_items

    def get_updated_runner_data(new_runner_data, frame_runner_data):
        updated_runner_data = {}
        for runner_data in new_runner_data:
            if "id" in runner_data and "id" in frame_runner_data:
                if runner_data["id"] == frame_runner_data["id"]:
                    updated_runner_data = runner_data

        return updated_runner_data
