#!/usr/bin/env python
from managers.WeatherManager import WeatherManager
from enums.Enums import WeatherFetch 

from datetime import datetime
class MoonPhaseManager():
    def moon_phase():
        weather_data = WeatherManager.get_weather(WeatherFetch.CACHEONLY, 1, 1)
        moon_phase = weather_data["moon_phase"]

        index = phase_index(moon_phase)
        name = phase_name(index)
        icon = phase_icon(index)
        day_length = get_day_length(weather_data["sunrise_time"], weather_data["sunset_time"])

        return {
                "phase_index": index,
                "phase_name": name,
                "phase_icon": icon,
                "day_length": "Day Length: " + day_length
                }

def phase_index(pos):
    if pos == 0 or pos == 1:
        index = 0
    elif pos > 0 and pos < .25:
        index = 1
    elif pos == .25:
        index = 2
    elif pos > .25 and pos < .5:
        index = 3
    elif pos == .5:
        index = 4
    elif pos > .5 and pos < .75:
        index = 5
    elif pos == .75:
        index = 6
    elif pos > .75 and pos < 1:
        index = 7
    else:
        index = 0

    return index

def phase_icon(index): 
    return {
        0: "new-moon", 
        1: "waxing-crecent-moon", 
        2: "first-quarter-moon", 
        3: "waxing-gibbous-moon", 
        4: "full-moon", 
        5: "waning-gibbous-moon", 
        6: "last-quarter-moon", 
        7: "waning-crescent-moon"
    }[index]

def phase_name(index):
    return {
        0: "New Moon", 
        1: "Waxing Crecent Moon", 
        2: "First Quarter Moon", 
        3: "Waxing Gibbous Moon", 
        4: "Full Moon", 
        5: "Waning Gibbous Moon", 
        6: "Last Quarter Moon", 
        7: "Waning Crescent Moon"
    }[index]

def get_day_length(sunrise, sunset):
    rise = datetime.fromtimestamp(sunrise)
    set = datetime.fromtimestamp(sunset)

    day_duration_seconds = (set - rise).seconds
    day_duration_hours = day_duration_seconds //3600
    day_duration_minutes = (day_duration_seconds //60 ) % 60

    return str(day_duration_hours).zfill(2) + ":" + str(day_duration_minutes).zfill(2)