#!/usr/bin/python3
import json
import sys
import os
from lib.utils import openConfigFile

class PeopleController:
    def __init__(self, peopleConfigFilename):
        #open config files
        configData = openConfigFile(peopleConfigFilename)
        self.people = configData["people"]
        self.intensities = configData["intensities"]

        return