#!/usr/bin/python3
""" Frame used to display time and date """

import time, os
from datetime import datetime
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout
from PyQt5.QtGui import QPixmap
from controllers.indoor_status_controller import IndoorStatusController
from controllers.moon_data_controller import MoonDataController
from obj.enums import Indoor_Status, Light_Status

LABLESTYLE_INDOOR_OPEN = "QLabel { color : white; font-size: 30px; border: 3px solid white; background: green;}"
LABLESTYLE_INDOOR_INUSE = "QLabel { color : white; font-size: 30px; border: 3px solid white; background: red;}"
LABLESTYLE_INDOOR_UNKNOWN = "QLabel { color : black; font-size: 20px; border: 3px solid white; background: yellow;}"
ICON_STYLESHEET = "QLabel { color : black; font-size: 30px; border: 0px none black; background: black;}"
LABLESTYLE = "QLabel { color : white; font-size: 30px;border: 0px solid black; background: black;}"
LABLETEXT_INDOOR_OPEN = "Indoor Free"
LABLETEXT_INDOOR_INUSE = "Indoor In Use!"
LABLETEXT_INDOOR_UNKNOWN = "Last Updated On: \n"
DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"

class TopFrame(QFrame):
    """ class that defines the date and time frame"""
    def __init__(self):
        QFrame.__init__(self)

        self.indoorStatusController = IndoorStatusController()
        
        self.setStyleSheet(LABLESTYLE_INDOOR_UNKNOWN)
        frame_layout = QGridLayout()
        frame_layout.setAlignment(QtCore.Qt.AlignTop)

        self.in_use_label = QLabel(LABLETEXT_INDOOR_UNKNOWN + datetime.min.strftime(DATE_FORMAT))
        
        self.wifi_icon_label = QLabel()
        self.wifi_icon_label.setStyleSheet(ICON_STYLESHEET)
        self.ble_icon_label = QLabel()
        self.ble_icon_label.setStyleSheet(ICON_STYLESHEET)
        self.lights_on_icon_label = QLabel()
        self.lights_on_icon_label.setStyleSheet(ICON_STYLESHEET)
        self.lights_off_icon_label = QLabel()
        self.lights_off_icon_label.setStyleSheet(ICON_STYLESHEET)
        self.warning_lights_icon_label = QLabel()
        self.warning_lights_icon_label.setStyleSheet(ICON_STYLESHEET)
        self.datetime_optional = QLabel()
        self.datetime_optional.setStyleSheet(LABLESTYLE)
        
        frame_layout.addWidget(self.in_use_label, 0, 0)
        frame_layout.addWidget(self.wifi_icon_label, 0, 1)
        frame_layout.addWidget(self.ble_icon_label, 0, 2)
        frame_layout.addWidget(self.lights_on_icon_label, 0, 3)
        frame_layout.addWidget(self.lights_off_icon_label, 0, 3)
        frame_layout.addWidget(self.warning_lights_icon_label, 0, 3)
        frame_layout.addWidget(self.datetime_optional, 0, 4)

        self.setLayout(frame_layout)
        self.setup_icons()
        data = IndoorStatusController.get_indoor_status()

        self.update_top_frame(data)

    def update_top_frame(self, data):
        self.update_date()
        self.update_indoor_status(data)

    def update_date(self):
        """ Date Stuff """
        self.datetime_optional.setText(time.strftime("%b %-d %Y"))

    def update_indoor_status(self, data):
        """ Updates the status of the indoor """
        styleSheetToUse = ""
        textToUse = ""

        self.datetime_optional.hide()

        self.indoorStatusController.update_statuses(data)
        indoor_status = self.indoorStatusController.Indoor_Status

        if indoor_status == Indoor_Status.NONE:
            self.in_use_label.hide()
            self.manage_icons(indoor_status, Light_Status.UNKNOWN)
            self.datetime_optional.show()
            return
        elif indoor_status == Indoor_Status.UNKNOWN:
            styleSheetToUse = LABLESTYLE_INDOOR_UNKNOWN
            textToUse = LABLETEXT_INDOOR_UNKNOWN
        elif (indoor_status == Indoor_Status.BLUETOOTH or
                indoor_status == Indoor_Status.WIFI or 
                indoor_status == Indoor_Status.WIFIANDBLUETOOTH):
            styleSheetToUse = LABLESTYLE_INDOOR_INUSE
            textToUse = LABLETEXT_INDOOR_INUSE
        elif indoor_status == Indoor_Status.FREE:
            textToUse = LABLETEXT_INDOOR_OPEN
            styleSheetToUse = LABLESTYLE_INDOOR_OPEN
        
        if self.indoorStatusController.dataHasExpired:
            textToUse = LABLETEXT_INDOOR_UNKNOWN + self.indoorStatusController.lastUpdatedOn.strftime(DATE_FORMAT)
            styleSheetToUse = LABLESTYLE_INDOOR_UNKNOWN

        self.manage_icons(indoor_status, self.indoorStatusController.Light_Status)
        self.setStyleSheet(styleSheetToUse)
        self.in_use_label.setText(textToUse)

    def setup_icons(self):
        DIRNAME = os.path.dirname(__file__)
        icon_size = 40
        
        wifi_icon = os.path.join(DIRNAME, "../assets/wi-fi-connected.png")
        ble_icon = os.path.join(DIRNAME, "../assets/bluetooth-2.png")
        light_on_icon = os.path.join(DIRNAME, "../assets/light-on.png")
        light_off_icon = os.path.join(DIRNAME, "../assets/light-off.png")
        light_warning_icon = os.path.join(DIRNAME, "../assets/hazard-warning-flasher--v2.png")

        image = QPixmap(wifi_icon)
        small_image = image.scaled(icon_size,
                                icon_size,
                                QtCore.Qt.KeepAspectRatio,
                                QtCore.Qt.FastTransformation)
        self.wifi_icon_label.setPixmap(small_image)

        image = QPixmap(ble_icon)
        small_image = image.scaled(icon_size,
                                icon_size,
                                QtCore.Qt.KeepAspectRatio,
                                QtCore.Qt.FastTransformation)
        self.ble_icon_label.setPixmap(small_image)

        image = QPixmap(light_on_icon)
        small_image = image.scaled(icon_size,
                                icon_size,
                                QtCore.Qt.KeepAspectRatio,
                                QtCore.Qt.FastTransformation)
        self.lights_on_icon_label.setPixmap(small_image)

        image = QPixmap(light_off_icon)
        small_image = image.scaled(icon_size,
                                icon_size,
                                QtCore.Qt.KeepAspectRatio,
                                QtCore.Qt.FastTransformation)
        self.lights_off_icon_label.setPixmap(small_image)

        image = QPixmap(light_warning_icon)
        small_image = image.scaled(icon_size,
                                icon_size,
                                QtCore.Qt.KeepAspectRatio,
                                QtCore.Qt.FastTransformation)
        self.warning_lights_icon_label.setPixmap(small_image)

    def manage_icons(self, indoor_status, light_status):
        if indoor_status == Indoor_Status.NONE:
            self.warning_lights_icon_label.hide()
            self.lights_on_icon_label.hide()
            self.lights_off_icon_label.hide()
            self.wifi_icon_label.hide()
            self.ble_icon_label.hide()
            return

        wifi_detected = indoor_status == Indoor_Status.WIFI or indoor_status == Indoor_Status.WIFIANDBLUETOOTH
        ble_detected = indoor_status == Indoor_Status.BLUETOOTH or indoor_status == Indoor_Status.WIFIANDBLUETOOTH
        lights_on = light_status == Light_Status.ON

        # display wifi and bluetooth icons when detected
        if wifi_detected:
            self.wifi_icon_label.show()
        else:
            self.wifi_icon_label.hide()

        if ble_detected:
            self.ble_icon_label.show()
        else:
            self.ble_icon_label.hide()

        # display correct lighting icon
        if (not wifi_detected) and (not ble_detected) and lights_on:
            self.warning_lights_icon_label.show()
            self.lights_on_icon_label.hide()
            self.lights_off_icon_label.hide()
        elif lights_on:
            self.warning_lights_icon_label.hide()
            self.lights_on_icon_label.show()
            self.lights_off_icon_label.hide()
        else:
            self.warning_lights_icon_label.hide()
            self.lights_on_icon_label.hide()
            self.lights_off_icon_label.show()

        #Temp: Will remove when we can sense the lights
        self.warning_lights_icon_label.hide()
        self.lights_on_icon_label.hide()
        self.lights_off_icon_label.hide()