#!/usr/bin/python3
""" Sets up and displays the running clothes for each person"""

import os
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout, QGroupBox
from PyQt5.QtGui import QPixmap

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
    def __init__(self, people_config_filename, temp_adjust_config_filename, weather_config_json):
        """ Initializes all of the things needed for this frame"""
        QFrame.__init__(self)
        self.setStyleSheet(LABLE_STYLE)
        self.runner_widget_list = []
        frame_lyout = QGridLayout()
        frame_lyout.setAlignment(QtCore.Qt.AlignTop)

        temp_adjust_config = open_config_file(temp_adjust_config_filename)

        people_controller = PeopleController(people_config_filename)

        sunrise_sunset = Sun(lat=weather_config_json["latitude"],
                             long=weather_config_json["longitude"])

        wind = get_wind(weather_config_json["currently"]["windSpeed"],
                        temp_adjust_config["wind_speed"])

        runner_row = 1
        for runner in people_controller.people:
            # loop through each runner and make their Frame
            runner_frame = QFrame()

            runner_layout = QGridLayout()
            runner_layout.setAlignment(QtCore.Qt.AlignTop)

            runner_name = QLabel(runner["name"])
            runner_name.setStyleSheet("QLabel { color: green; "
                                      "font-size: 35px; "
                                      "font-weight: bold; "
                                      "text-decoration: underline;}")
            runner_layout.addWidget(runner_name, 0, 0)

            col = 0
            row = 0

            for intensity in people_controller.intensities:
                # for each runner we then have to loop through each intensity
                # and calculate adjusted temperature and clothing
                temp_adjuster = TemperatureAdjustmentController(sunrise_sunset.time_of_day(),
                                                                weather_config_json["currently"]["icon"],
                                                                wind, runner["gender"],
                                                                runner["feel"],
                                                                intensity["type"],
                                                                weather_config_json["currently"]["temperature"],
                                                                temp_adjust_config)
                clothing_controller = ClothingController(temp_adjuster.adjusted_temperature,
                                                         CLOTHING_CONFIG_FILENAME, runner["gender"], 
                                                         intensity["type"],
                                                         weather_config_json["currently"]["icon"],
                                                         sunrise_sunset.time_of_day())
                clothes = clothing_controller.calculate_items()

                # degree_sign= u'\N{DEGREE SIGN}'
                intensity_frame = QGroupBox(intensity["name"])
                intensity_layout = QGridLayout()
                intensity_layout.setAlignment(QtCore.Qt.AlignTop)

                for body_part in clothes:
                    # once we have the calculated clothing for a runner for an intensity
                    # we add it to the UI
                    row += 1
                    item = QLabel(clothes[body_part])
                    intensity_layout.addWidget(item, row, 0)

                intensity_frame.setLayout(intensity_layout)
                runner_layout.addWidget(intensity_frame, 1, col)
                col += 1

            runner_frame.setLayout(runner_layout)
            frame_lyout.addWidget(runner_frame, runner_row, 0)
            self.runner_widget_list.append(runner_frame)
            runner_row += 1

            # we only want to show the first runner initially
            # so every runner after the first gets set to invisible
            if runner_row > 2:
                runner_frame.setVisible(False)

        self.setLayout(frame_lyout)

def get_wind(wind_speed, wind_speed_config):
    """
    Take the wind speed and calculate the wind type
    TODO: This should be someplace else!
    """
    if wind_speed_config["light_min"] <= wind_speed <= wind_speed_config["light_max"]:
        return "light_wind"
    elif wind_speed_config["wind_min"] <= wind_speed <= wind_speed_config["wind_max"]:
        return "windy"
    elif wind_speed_config["heavy_min"] <= wind_speed <= wind_speed_config["heavy_max"]:
        return "heavy_wind"