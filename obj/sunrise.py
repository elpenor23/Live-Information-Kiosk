"""
This module deals with calculating sunrises and sunsets
and determining if it is day/night/duck/dawn
"""
import logging
from math import cos, sin, acos, asin, tan
from math import degrees as deg, radians as rad
from datetime import date, datetime, time, timedelta
from dateutil import tz
from time import mktime

# this module is not provided here. See text.
#from timezone import LocalTimezone

class Sun():
    """
    Calculate sunrise and sunset based on equations from NOAA
    http://www.srrb.noaa.gov/highlights/sunrise/calcdetails.html

    typical use, calculating the sunrise at the present day:

    import datetime
    import sunrise
    s = sun(lat=49,long=3)
    print('sunrise at ',s.sunrise(when=datetime.datetime.now())
    """
    def __init__(self, lat=52.37, long=4.90): # default Amsterdam
        self.logger = logging.getLogger('kiosk_log')
        self.lat = lat
        self.long = long
        self.from_timezone = tz.tzutc()
        self.to_timezone = tz.tzlocal()
        self.day = None
        self.time = None
        self.timezone = None

    def sunrise(self, when=None):
        """
        return the time of sunrise as a datetime.time object
        when is a datetime.datetime object. If none is given
        a local time zone is assumed (including daylight saving
        if present)
        """
        if when is None:
            when = datetime.now(tz=self.to_timezone)
        self.__preptime(when)
        self.__calc()
        return self.__timefromdecimalday(self.sunrise_t)

    def sunset(self, when=None):
        """ Gets sunset """
        if when is None:
            when = datetime.now(tz=self.to_timezone)
        self.__preptime(when)
        self.__calc()
        return self.__timefromdecimalday(self.sunset_t)

    def solarnoon(self, when=None):
        """ Gets solar noon """
        if when is None:
            when = datetime.now(tz=self.to_timezone)
        self.__preptime(when)
        self.__calc()
        return self.__timefromdecimalday(self.solarnoon_t)

    def is_dusk(self, when=None):
        """ checks if it is dusk """
        if when is None:
            when = datetime.now(tz=self.to_timezone)
        sunset = self.sunset(when)
        sunset_full_date = datetime.strptime(when.strftime("%m/%d/%Y ") + sunset.strftime("%H:%M:%S"), "%m/%d/%Y %H:%M:%S")
        sunset_full_date.replace(tzinfo = self.to_timezone)

        thirty_min_before_sunset = (sunset_full_date + timedelta(minutes=-30)).replace(tzinfo=self.to_timezone)
        thirty_min_after_sunset = (sunset_full_date + timedelta(minutes=30)).replace(tzinfo=self.to_timezone)

        self.logger.debug(f'is_dusk?\nthirty_min_before_sunset:{thirty_min_before_sunset}\n<=\nwhen:{when}\n<=\nthirty_min_after_sunset:{thirty_min_after_sunset}')
        return thirty_min_before_sunset <= when <= thirty_min_after_sunset

    def is_dawn(self, when=None):
        """ checks if it is dawn """
        if when is None:
            when = datetime.now(tz=self.to_timezone)
        sunrise = self.sunrise(when)
        sunrise_full_date = datetime.strptime(when.strftime("%m/%d/%Y ") + sunrise.strftime("%H:%M:%S"), "%m/%d/%Y %H:%M:%S")
        sunrise_full_date.replace(tzinfo=self.to_timezone)

        thirty_min_before_sunrise = (sunrise_full_date + timedelta(minutes=-30)).replace(tzinfo=self.to_timezone)
        thirty_min_after_sunrise = (sunrise_full_date + timedelta(minutes=30)).replace(tzinfo=self.to_timezone)

        self.logger.debug(f'is_dawn?\nthirty_min_before_sunrise:{thirty_min_before_sunrise}\n<=\nwhen:{when}\n<=\thirty_min_after_sunrise:{thirty_min_after_sunrise}')
        return thirty_min_before_sunrise <= when <= thirty_min_after_sunrise

    def is_day(self, when=None):
        """ checks if it is day """
        if when is None:
            when = datetime.now(tz=self.to_timezone)
        sunrise = self.sunrise(when)
        sunrise_full_date = datetime.strptime(when.strftime("%m/%d/%Y ") + sunrise.strftime("%H:%M:%S"), "%m/%d/%Y %H:%M:%S")
        sunrise_timezone = sunrise_full_date.replace(tzinfo=self.to_timezone)

        sunset = self.sunset(when)
        sunset_full_date = datetime.strptime(when.strftime("%m/%d/%Y ") + sunset.strftime("%H:%M:%S"), "%m/%d/%Y %H:%M:%S")
        sunset_timezone = sunset_full_date.replace(tzinfo=self.to_timezone)

        self.logger.debug(f'is_day?\nsunrise_timezone:{sunrise_timezone}\n>=\nwhen:{when}\n<=\nsunset_timezone):{sunset_timezone}')
        return sunrise_timezone <= when <= sunset_timezone

    def is_night(self, when=None):
        """ checks if it is night """
        if when is None:
            when = datetime.now(tz=self.to_timezone)
        sunset = self.sunset(when)
        sunset_full_date = datetime.strptime(when.strftime("%m/%d/%Y ") + sunset.strftime("%H:%M:%S"), "%m/%d/%Y %H:%M:%S")
        sunset_timezone = sunset_full_date.replace(tzinfo=self.to_timezone)

        return when >= sunset_timezone

    def time_of_day(self, when=None):
        """
        returns if it is:
        dusk, dawn, day or night
        """
        if when is None:
            when = datetime.now(tz=self.to_timezone)

        self.logger.debug(f'When: {when}')
        if self.is_dawn(when):
            return "dawn"
        elif self.is_dusk(when):
            return "dusk"
        elif self.is_day(when):
            return "day"
        elif self.is_night(when):
            return "night"
        else:
            return "unknown"

    @staticmethod
    def __timefromdecimalday(day):
        """
        returns a datetime.time object.
        day is a decimal day between 0.0 and 1.0, e.g. noon = 0.5
        """
        hours = 24.0*day
        full_hours = int(hours)
        minutes = (hours-full_hours)*60
        full_minutes = int(minutes)
        seconds = (minutes-full_minutes)*60
        remaining_seconds = int(seconds)
        return time(hour=full_hours, minute=full_minutes, second=remaining_seconds)

    def __preptime(self, when):
        """
        Extract information in a suitable format from when, 
        a datetime.datetime object.
        """
        # datetime days are numbered in the Gregorian calendar
        # while the calculations from NOAA are distibuted as
        # OpenOffice spreadsheets with days numbered from
        # 1/1/1900. The difference are those numbers taken for 
        # 18/12/2010
        self.day = when.toordinal()-(734124-40529)
        t = when.time()
        self.time = (t.hour + t.minute/60.0 + t.second/3600.0)/24.0

        self.timezone = 0
        offset = when.utcoffset()
        if not offset is None:
            self.timezone = offset.seconds/3600.0  + (offset.days * 24)

    def __calc(self):
        """
        Perform the actual calculations for sunrise, sunset and
        a number of related quantities.

        The results are stored in the instance variables
        sunrise_t, sunset_t and solarnoon_t
        """
        timezone = self.timezone # in hours, east is positive
        longitude = self.long     # in decimal degrees, east is positive
        latitude = self.lat      # in decimal degrees, north is positive

        time = self.time # percentage past midnight, i.e. noon  is 0.5
        day = self.day     # daynumber 1=1/1/1900
        
        Jday = day+2415018.5+time-timezone/24 # Julian day
        Jcent = (Jday-2451545)/36525    # Julian century

        Manom = 357.52911+Jcent*(35999.05029-0.0001537*Jcent)
        Mlong = 280.46646+Jcent*(36000.76983+Jcent*0.0003032)%360
        Eccent = 0.016708634-Jcent*(0.000042037+0.0001537*Jcent)
        Mobliq = 23+(26+((21.448-Jcent*(46.815+Jcent*(0.00059-Jcent*0.001813))))/60)/60
        obliq = Mobliq+0.00256*cos(rad(125.04-1934.136*Jcent))
        vary = tan(rad(obliq/2))*tan(rad(obliq/2))
        Seqcent = sin(rad(Manom))*(1.914602-Jcent*(0.004817+0.000014*Jcent))+sin(rad(2*Manom))*(0.019993-0.000101*Jcent)+sin(rad(3*Manom))*0.000289
        Struelong = Mlong+Seqcent
        Sapplong = Struelong-0.00569-0.00478*sin(rad(125.04-1934.136*Jcent))
        declination = deg(asin(sin(rad(obliq))*sin(rad(Sapplong))))

        eqtime = 4*deg(vary*sin(2*rad(Mlong))-2*Eccent*sin(rad(Manom))+4*Eccent*vary*sin(rad(Manom))*cos(2*rad(Mlong))-0.5*vary*vary*sin(4*rad(Mlong))-1.25*Eccent*Eccent*sin(2*rad(Manom)))

        hourangle = deg(acos(cos(rad(90.833))/(cos(rad(latitude))*cos(rad(declination)))-tan(rad(latitude))*tan(rad(declination))))

        self.solarnoon_t = (720-4*longitude-eqtime+timezone*60)/1440
        self.sunrise_t = self.solarnoon_t-hourangle*4/1440
        self.sunset_t = self.solarnoon_t+hourangle*4/1440
