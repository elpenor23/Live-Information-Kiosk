from enum import Enum

class Indoor_Status(Enum):
    NONE = 1
    UNKNOWN = 2
    BLUETOOTH = 3
    WIFI = 4
    WIFIANDBLUETOOTH = 5
    FREE = 6

class Light_Status(Enum):
    UNKNOWN = 1
    ON = 2
    OFF = 3