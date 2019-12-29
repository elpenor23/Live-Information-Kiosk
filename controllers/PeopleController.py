#!/usr/bin/python3
import json
import sys
import os

class PeopleController:
    def __init__(self, peopleConfigFilename):
        #open config files
        configData = self.openConfigFile(peopleConfigFilename)
        self.people = configData["people"]
        self.intensities = configData["intensities"]

        return

    def openConfigFile(self, configFileName):
        try:
            configFile = open(configFileName, 'r')
        except IOError as ex:
            errorText = "Could not read config file: " + configFileName
            print(errorText)
            print(ex)
            sys.exit()

        #get the data
        configData = json.loads(configFile.read())
        configFile.close
        return configData