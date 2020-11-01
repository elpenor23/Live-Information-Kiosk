#!/usr/bin/env python
"""
moonphase.py - Calculate Lunar Phase
Author: Sean B. Palmer, inamidst.com
Cf. http://en.wikipedia.org/wiki/Lunar_phase#Lunar_phase_calculation
"""

import math, decimal, datetime
dec = decimal.Decimal

class MoonPhaseManager():
    def moon_phase(): 
        pos = position()
        index = phase_index(pos)
        name = phase_name(index)
        icon = phase_icon(index)

        return {
                "phase_index": index,
                "phase_name": name,
                "phase_icon": icon
                }

def position(now=None): 
    if now is None: 
        now = datetime.datetime.now()

    diff = now - datetime.datetime(2001, 1, 1)
    days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
    lunations = dec("0.20439731") + (days * dec("0.03386319269"))

    return lunations % dec(1)

def phase_index(pos):
    index = (pos * dec(8)) + dec("0.5")
    index = math.floor(index)
    return int(index) & 7

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