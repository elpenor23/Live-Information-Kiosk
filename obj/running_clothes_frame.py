#!/usr/bin/python3
""" Sets up and displays the running clothes for each person"""
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout, QGroupBox
from controllers.running_clothes_controller import RunningClothesController

from lib.utils import get_api_data

LABLE_STYLE = ("QLabel { color : white; font-size: 30px;} "
               "QGroupBox { color : white; font-size: 30px; "
               "font-weight: bold; margin-top: 1.5ex; border: 2px "
               "solid gray; border-radius: 3px; } QGroupBox::title "
               "{ subcontrol-origin: margin;subcontrol-position: top left; "
               "/* position at the top center */ padding: 0 8px; font-weight: bold;}")

class RunningClothes(QFrame):
    """ Class that displays the runnsers clothing"""
    def __init__(self):
        """ Initializes all of the things needed for this frame"""
        QFrame.__init__(self)
        self.setStyleSheet(LABLE_STYLE)
        self.runner_widget_list = []
        main_layout = QGridLayout()
        self.main_frame = QFrame()

        self.build_runner_layout()

        main_layout.addWidget(self.main_frame, 0, 0)
        self.setLayout(main_layout)

    def build_runner_layout(self):
        """ Build the layout with all the runner frames in it """

        frame_layout = QGridLayout()
        frame_layout.setAlignment(QtCore.Qt.AlignTop)

        runner_row = 1
        runner_data = RunningClothesController.get_runner_data()
        all_items = RunningClothesController.get_all_items()

        for runner in runner_data:

            runner_frame = self.build_runner_frame(runner, all_items)

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

    def build_runner_frame(self, runner, all_items):
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
        runner_id = QLabel("id:" + runner["id"])
        runner_id.hide()

        runner_layout.addWidget(runner_gender, 0, 0)
        runner_layout.addWidget(runner_feel, 0, 0)
        runner_layout.addWidget(runner_id, 0, 0)

        col = 0
        #row = 0

        for clothing_data in runner["data"]:
            # for each runner we then have to loop through each intensity
            # and calculate adjusted temperature and clothing

            intensity_frame = self.build_intensity_frame(clothing_data, all_items)

            runner_layout.addWidget(intensity_frame, 1, col)
            col += 1

        runner_frame.setLayout(runner_layout)

        return runner_frame

    def build_intensity_frame(self, clothing_data, all_items):
        """ builds each intensity frame """
        intensity_layout = QGridLayout()
        intensity_layout.setAlignment(QtCore.Qt.AlignTop)

        intensity_frame = QGroupBox(clothing_data["intensity"])

        item_row = 0
        #add all items to the UI but make them hidden
        for item in all_items["data"]:
            item_row += 1
            item_widget = QLabel(all_items["data"][item]["title"])
            item_widget.hide()
            intensity_layout.addWidget(item_widget, item_row, 0)

        #add hidden values for future use
        intensity_type = QLabel("type:" + clothing_data["intensity_type"])
        intensity_type.hide()
        intensity_layout.addWidget(intensity_type, 0, 0)

        intensity_frame.setLayout(intensity_layout)

        #now only show the ones we need
        self.show_correct_clothing(intensity_frame, clothing_data["clothes"])
            
        return intensity_frame

    def show_correct_clothing(self, intensity_frame, intensity_clothing):
        """displays the correct clothing for the current weather """
        for body_part in intensity_clothing:
            # once we have the calculated clothing for a runner for an intensity
            # we show it on the UI
            for child in intensity_frame.findChildren(QLabel):
                if intensity_clothing[body_part] == child.text():
                    child.show()
