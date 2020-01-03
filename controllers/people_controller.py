#!/usr/bin/python3
"""
Gets the people and intensities from the config
It will eventually do more
"""
from lib.utils import open_config_file

class PeopleController:
    def __init__(self, people_config_filename):
        #open config files
        config_data = open_config_file(people_config_filename)
        self.people = config_data["people"]
        self.intensities = config_data["intensities"]

        return