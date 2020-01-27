#!/usr/bin/python3
""" Sets up and displays the running clothes for each person"""

import os
import logging
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout, QGroupBox

from controllers.people_controller import PeopleController
from controllers.temperature_adjustment_controller import TemperatureAdjustmentController
from controllers.clothing_controller import ClothingController
from lib.utils import open_config_file
from obj.sunrise import Sun

LABLE_STYLE = ("QLabel { color : white; font-size: 30px;} "
               "QGroupBox { color : white; font-size: 30px; "
               "font-weight: bold; margin-top: 1.5ex; border: 2px "
               "solid gray; border-radius: 3px; } QGroupBox::title "
               "{ subcontrol-origin: margin;subcontrol-position: top left; "
               "/* position at the top center */ padding: 0 8px; font-weight: bold;}")

DIRNAME = os.path.dirname(__file__)
CLOTHING_CONFIG_FILENAME = os.path.join(DIRNAME, "../config/clothingConfig.json")

class RunningClothes(QFrame):
    """ Class that displays the runnsers clothing"""
    def __init__(self, people_config_filename, temp_adjust_config_filename, weather_object):
        """ Initializes all of the things needed for this frame"""
        QFrame.__init__(self)
        self.logger = logging.getLogger('kiosk_log')
        self.setStyleSheet(LABLE_STYLE)
        self.runner_widget_list = []
        self.frame_layout = None

        temp_adjust_config = open_config_file(temp_adjust_config_filename)

        self.people_controller = PeopleController(people_config_filename)

        self.build_runner_layout(weather_object, temp_adjust_config)

    def build_runner_layout(self, weather_object, temp_adjust_config):
        """ Build the layout with all the runner frames in it """
        self.logger.info(f'build_runner_layout')

        sunrise_sunset = Sun(lat=weather_object["latitude"],
                                long=weather_object["longitude"])

        wind = get_wind(weather_object["currently"]["windSpeed"],
                        temp_adjust_config["wind_speed"])

        self.frame_layout = QGridLayout()
        self.frame_layout.setAlignment(QtCore.Qt.AlignTop)
        runner_row = 1
        for runner in self.people_controller.people:
            
            self.logger.info(f"making runner frame: {runner}")

            runner_frame = build_runner_frame(runner,
                                                wind,
                                                weather_object,
                                                temp_adjust_config,
                                                sunrise_sunset.time_of_day(),
                                                self.people_controller,
                                                self.logger)

            self.runner_widget_list.append(runner_frame)
            runner_row += 1

            # we only want to show the first runner initially
            # so every runner after the first gets set to invisible
            if runner_row > 2:
                runner_frame.setVisible(False)

            self.frame_layout.addWidget(runner_frame, runner_row, 0)
        
        self.setLayout(self.frame_layout)

def build_runner_frame(runner, wind, weather_object, temp_adjust_config, time_of_day, people_controller, logger):
    """ build each runner frame """
    # loop through each runner and make their Frame
    runner_frame = QFrame()

    runner_layout = QGridLayout()
    runner_layout.setAlignment(QtCore.Qt.AlignTop)

    runner_name = QLabel(runner["name"])
    runner_name.setStyleSheet("QLabel { color: " + runner['color'] + "; "
                              "font-size: 35px; "
                              "font-weight: bold; "
                              "text-decoration: underline;}")
    runner_layout.addWidget(runner_name, 0, 0)

    col = 0
    #row = 0

    for intensity in people_controller.intensities:
        # for each runner we then have to loop through each intensity
        # and calculate adjusted temperature and clothing

        logger.info(f"looping through intensities: {intensity}")
        intensity_frame = build_intensity_frame(intensity,
                                                runner,
                                                wind,
                                                weather_object,
                                                temp_adjust_config,
                                                time_of_day,
                                                logger)

        runner_layout.addWidget(intensity_frame, 1, col)
        col += 1

    runner_frame.setLayout(runner_layout)

    return runner_frame

def build_intensity_frame(intensity, runner, wind, weather_object, temp_adjust_config, time_of_day, logger):
    """ builds each intensity frame """

    temp_adjuster = TemperatureAdjustmentController(time_of_day,
                                                    weather_object["currently"]["icon"],
                                                    wind,
                                                    runner["gender"],
                                                    runner["feel"],
                                                    intensity["type"],
                                                    weather_object["currently"]["temperature"],
                                                    temp_adjust_config)
    clothing_controller = ClothingController(temp_adjuster.adjusted_temperature,
                                             CLOTHING_CONFIG_FILENAME, runner["gender"],
                                             intensity["type"],
                                             weather_object["currently"]["icon"],
                                             time_of_day)
    clothes = clothing_controller.calculate_items()

    intensity_layout = QGridLayout()
    intensity_layout.setAlignment(QtCore.Qt.AlignTop)

    intensity_frame = QGroupBox(intensity["name"])
    row = 0
    for body_part in clothes:
        logger.debug(f"body part: {body_part}")
        # once we have the calculated clothing for a runner for an intensity
        # we add it to the UI
        row += 1
        item = QLabel(clothes[body_part])
        intensity_layout.addWidget(item, row, 0)

    intensity_frame.setLayout(intensity_layout)

    return intensity_frame

def get_wind(wind_speed, wind_speed_config):
    """
    Take the wind speed and calculate the wind type
    TODO: This should be someplace else!
    """
    return_value = "None"
    if wind_speed_config["light_min"] <= wind_speed <= wind_speed_config["light_max"]:
        return_value = "light_wind"
    elif wind_speed_config["wind_min"] <= wind_speed <= wind_speed_config["wind_max"]:
        return_value = "windy"
    elif wind_speed_config["heavy_min"] <= wind_speed <= wind_speed_config["heavy_max"]:
        return_value = "heavy_wind"

    return return_value
