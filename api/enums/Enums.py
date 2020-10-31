from enum import Enum

class WeatherFetch(Enum):
    CACHEONLY = 1
    FORCEREFRESH = 2
    NORMAL = 3
