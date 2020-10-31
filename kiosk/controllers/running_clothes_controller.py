from lib.utils import open_config_file, get_api_data, PEOPLE_CONFIG_FILENAME, LOCATION_CONFIG_FILENAME
CLOTHING_API_ENDPOINT = "clothing"

class RunningClothesController():
    
    def get_runner_data():
        people = open_config_file(PEOPLE_CONFIG_FILENAME)
        location = open_config_file(LOCATION_CONFIG_FILENAME)
        
        #parms
        names = ""
        feels = ""
        genders = ""
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

            if genders != "":
                genders += ','
            genders += person["gender"]

            if colors != "":
                colors += ','
            colors += person["color"]

        params = {
            'type': "calculate", 
            "lat": location["latitude"],
            "lon": location["longitude"],
            "ids": ids,
            "feels": feels,
            "genders": genders,
            "names": names,
            "colors": colors
        }

        results = get_api_data(CLOTHING_API_ENDPOINT, params)

        return results

    def get_all_items():
        params = {'type': "allclothes"}
        all_items = get_api_data(CLOTHING_API_ENDPOINT, params)
        return all_items

    def get_updated_runner_data(new_runner_data, frame_runner_data):
        updated_runner_data = {}
        for runner_data in new_runner_data:
            if runner_data["id"] == frame_runner_data["id"]:
                updated_runner_data = runner_data

        return updated_runner_data
