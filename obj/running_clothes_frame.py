#!/usr/bin/python3
""" Sets up and displays the running clothes for each person"""

import os
import datetime
from datetime import timezone
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
        main_layout = QGridLayout()
        self.main_frame = QFrame()
        
        self.temp_adjust_config_filename = temp_adjust_config_filename

        self.people_controller = PeopleController(people_config_filename)

        self.clothing_controller = ClothingController(CLOTHING_CONFIG_FILENAME)

        self.build_runner_layout(weather_object)

        main_layout.addWidget(self.main_frame, 0, 0)
        self.setLayout(main_layout)

    def build_runner_layout(self, weather_object):
        """ Build the layout with all the runner frames in it """
        self.logger.info(f'build_runner_layout')

        frame_layout = QGridLayout()
        frame_layout.setAlignment(QtCore.Qt.AlignTop)
        runner_row = 1
        for runner in self.people_controller.people:
            
            self.logger.info(f"making runner frame: {runner}")

            runner_frame = self.build_runner_frame(runner,
                                                weather_object,
                                                self.people_controller,
                                                self.logger)

            self.runner_widget_list.append(runner_frame)
            runner_row += 1

            # we only want to show the first runner initially
            # so every runner after the first gets set to invisible
            if runner_row > 2:
                runner_frame.setVisible(False)

            frame_layout.addWidget(runner_frame, runner_row, 0)
        
        self.main_frame.setLayout(frame_layout)

    def hide_all_clothing(self, intensity_frame):
        for child in intensity_frame.findChildren(QLabel):
            child.hide()

    def build_runner_frame(self, runner, weather_object, people_controller, logger):
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

        #add hidden values we need for future use
        runner_gender = QLabel("gender:" + runner["gender"])
        runner_gender.hide()
        runner_feel = QLabel("feel:" + runner["feel"])
        runner_feel.hide()

        runner_layout.addWidget(runner_gender, 0, 0)
        runner_layout.addWidget(runner_feel, 0, 0)

        col = 0
        #row = 0

        for intensity in people_controller.intensities:
            # for each runner we then have to loop through each intensity
            # and calculate adjusted temperature and clothing

            logger.info(f"looping through intensities: {intensity}")
            intensity_frame = self.build_intensity_frame(intensity,
                                                    runner,
                                                    weather_object,
                                                    logger)

            runner_layout.addWidget(intensity_frame, 1, col)
            col += 1

        runner_frame.setLayout(runner_layout)

        return runner_frame

    def build_intensity_frame(self, intensity, runner, weather_object, logger):
        """ builds each intensity frame """
        all_items = self.clothing_controller.get_all_items()

        intensity_layout = QGridLayout()
        intensity_layout.setAlignment(QtCore.Qt.AlignTop)

        intensity_frame = QGroupBox(intensity["name"])

        item_row = 0
        #add all items to the UI but make them hidden
        for item in all_items:
            #print(item)
            item_row += 1
            item_widget = QLabel(item)
            item_widget.hide()
            intensity_layout.addWidget(item_widget, item_row, 0)

        #add hidden values for future use
        intensity_type = QLabel("type:" + intensity["type"])
        intensity_type.hide()
        intensity_layout.addWidget(intensity_type, 0, 0)

        intensity_frame.setLayout(intensity_layout)

        #now only show the ones we need
        self.show_correct_clothing(intensity_frame, intensity, runner, weather_object)
            
        return intensity_frame

    def show_correct_clothing(self, intensity_frame, intensity, runner, weather_object):
        """displays the correct clothing for the current weather """
        weather_time = datetime.datetime.fromtimestamp(weather_object["current"]["dt"])
        weather_time = weather_time.replace(tzinfo=timezone.utc)

        sunrise_sunset = Sun(lat=weather_object["lat"],
                             long=weather_object["lon"])
        time_of_day = sunrise_sunset.time_of_day(weather_time)

        temp_adjuster = TemperatureAdjustmentController(time_of_day,
                                                        weather_object["current"]["weather"][0]["main"],
                                                        weather_object["current"]["wind_speed"],
                                                        runner["gender"],
                                                        runner["feel"],
                                                        intensity["type"],
                                                        weather_object["current"]["temp"],
                                                        self.temp_adjust_config_filename)

        clothes = self.clothing_controller.calculate_items(temp_adjuster.adjusted_temperature,
                                                runner["gender"],
                                                intensity["type"],
                                                weather_object["current"]["weather"][0]["main"],
                                                time_of_day)
        for body_part in clothes:
            # once we have the calculated clothing for a runner for an intensity
            # we show it on the UI
            for child in intensity_frame.findChildren(QLabel):
                if clothes[body_part] == child.text():
                    child.show()
