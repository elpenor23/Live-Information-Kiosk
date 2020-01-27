#!/usr/bin/python3
""" Sets up the UI and controls UI changes """

import os
import logging
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout
from obj.weather_frame import Weather
from obj.running_clothes_frame import RunningClothes
from update_thread import UpdateThread
from controllers.weather_controller import WeatherController
from lib.utils import open_config_file

DIRNAME = os.path.dirname(__file__)
LOCATION_CONFIG_FILENAME = os.path.join(DIRNAME, "config/locationConfig.json")
PEOPLE_CONFIG_FILENAME = os.path.join(DIRNAME, "config/peopleConfig.json")
TEMP_ADJUSTMENT_CONFIG_FILENAME = os.path.join(DIRNAME, "config/tempAdjustConfig.json")

class AppUI(QWidget):
    """ Sets up the up the UI """
    def __init__(self):
        super(AppUI, self).__init__()
        self.init_ui()

    #####################################
    # Start - Build All section of the UI
    #####################################
    # Add all the sections to the main window
    def init_ui(self):
        """ Initializes all the secions in the layout """
        self.logger = logging.getLogger('kiosk_log')

        window_layout = QGridLayout()
        window_layout.setAlignment(QtCore.Qt.AlignTop)

        self.weather_controller = WeatherController(LOCATION_CONFIG_FILENAME)
        self.weather_controller.parse_weather()

        self.weather_frame = Weather(self.weather_controller)
        window_layout.addWidget(self.weather_frame, 0, 0)

        self.running_clothes_frame = RunningClothes(PEOPLE_CONFIG_FILENAME,
                                                    TEMP_ADJUSTMENT_CONFIG_FILENAME,
                                                    self.weather_controller.weather_obj)
        window_layout.addWidget(self.running_clothes_frame, 1, 0)

        ui_palette = self.palette()
        ui_palette.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(ui_palette)

        #Set the layout and window
        self.setLayout(window_layout)
        self.move(300, 150)
        self.show()
        #start Fullscreen
        self.showFullScreen()

        # kick off the thread
        self.update_thread = UpdateThread()
        self.update_thread.update_clock.connect(self.callback_update_clock)
        self.update_thread.update_weather_and_clothes.connect(
            self.callback_update_weather_and_clothes)
        self.update_thread.update_person.connect(self.callback_update_person)
        self.update_thread.start()

    def callback_update_clock(self):
        """callback for updating the clock from the timing thread"""
        self.weather_frame.update_clock()

    def callback_update_person(self):
        """
        Callback for updateing the person frame from the timing thread.
        Makes the current visible person invisible and the next person visible.
        Loops around when it hits the end of the person list.
        """
        people = self.running_clothes_frame.runner_widget_list
        number_of_people = len(people)
        j = 0
        index_to_set_visible = 0
        while j < number_of_people:
            if people[j].isVisible():
                people[j].setVisible(False)
                index_to_set_visible = j + 1
            j += 1

        if index_to_set_visible > number_of_people - 1:
            index_to_set_visible = 0

        people[index_to_set_visible].setVisible(True)

    def callback_update_weather_and_clothes(self):
        """callback to update the weather and clothing from the timeing thread"""
        self.weather_controller.parse_weather()
        self.weather_frame.update_display(self.weather_controller)

        temp_adjust_config = open_config_file(TEMP_ADJUSTMENT_CONFIG_FILENAME)
        self.running_clothes_frame.build_runner_layout(self.weather_controller.weather_obj,
                                                       temp_adjust_config)

    def keyPressEvent(self, event):
        """
        handles key press event <Esc> closes and <return>
        switches from full screen to normal window
        """
        if str(event.key()) == str(QtCore.Qt.Key_Escape):
            self.close()
        elif str(event.key()) == str(QtCore.Qt.Key_Return):
            if self.isFullScreen():
                self.showNormal()
                self.setGeometry(300, 150, 500, 500)
            else:
                self.showFullScreen()
