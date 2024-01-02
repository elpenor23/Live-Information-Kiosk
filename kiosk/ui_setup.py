#!/usr/bin/python3
""" Sets up the UI and controls UI changes """

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QFrame, QGroupBox, QLabel
from obj.weather_frame import Weather
from obj.running_clothes_frame import RunningClothes
from update_thread import UpdateThread
from controllers.weather_controller import WeatherController
from controllers.running_clothes_controller import RunningClothesController

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

        window_layout = QGridLayout()
        window_layout.setAlignment(QtCore.Qt.AlignTop)

        self.weather_controller = WeatherController()
        self.weather_controller.parse_weather({})

        self.weather_frame = Weather(self.weather_controller)
        window_layout.addWidget(self.weather_frame, 0, 0)

        self.running_clothes_frame = RunningClothes()

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
        self.update_thread.update_data.connect(self.callback_update_data)
        self.update_thread.update_signal.connect(self.callback_update_signal)
        self.update_thread.start()

    #CALLBACKS FROM Update Thread
    def callback_update_signal(self, todo):
        if todo == "clock":
            self.weather_frame.update_clock()
        elif todo == "person":
            self.update_person()

    def callback_update_data(self, data):
        if data["api"] == "moon":
                self.weather_frame.update_moon(data["return"])
        elif data["api"] == "solar":
            self.weather_frame.update_solar(data["return"])
        elif data["api"] == "indoor":
            self.weather_frame.update_indoor_status(data["return"])
        elif data["api"] == "weather":
            self.update_weather_and_clothes(data["return"])


    def update_person(self):
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

    def update_weather_and_clothes(self, data):
        """callback to update the weather and clothing from the timeing thread"""
        self.weather_controller.parse_weather(data)
        self.weather_frame.update_display(self.weather_controller)
        
        running_frame = self.findChild(RunningClothes)
        self.update_clothing(running_frame)

    def update_clothing(self, running_frame):
        """Loops through the UI and hides the displayed clothing"""
        running_sub_frame = running_frame.findChild(QFrame)
        runner_frames = running_sub_frame.findChildren(QFrame)
        new_running_clothes_data = RunningClothesController.get_runner_data()

        for runner_frame in runner_frames:
            new_intensity_clothes_data = {}
            if runner_frame.__class__.__name__ == "QFrame":
                frame_runner_data = self.get_hidden_data(runner_frame)
                new_runner_data = RunningClothesController.get_updated_runner_data(new_running_clothes_data, frame_runner_data)

                intensity_frames = runner_frame.findChildren(QGroupBox)
                for intensity in intensity_frames:
                    intensity_frame_data = self.get_hidden_data(intensity)
                    if "data" in new_runner_data:
                        for new_intensity_data in new_runner_data["data"]:
                            if new_intensity_data["intensity_type"] == intensity_frame_data["type"]:
                                new_intensity_clothes_data = new_intensity_data["clothes"]

                        running_frame.hide_all_clothing(intensity)
                        running_frame.show_correct_clothing(intensity, new_intensity_clothes_data)

    def get_hidden_data(self, frame):
        """Gets data from hidden lables in frames"""
        data = {}
        for label in frame.findChildren(QLabel):
            if ":" in label.text():
                text = label.text().split(":")
                data[text[0]] =  text[1]
        return data

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
