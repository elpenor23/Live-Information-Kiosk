# Live Information Kiosk
Counter top kiosk meant to show you useful imformation that you need on the regular.

## Requirements
 - Python3
 - PyQt5 (pip3 install PyQt5)
 - dateutils (pip3 install python-dateutil)
 - requests (pip3 install requests)

# Modules
Current modules show:

    * Weather and time information
    * what to wear while running based on weather and person

Use:

    <return>    - Enters/Leaves Full Screen Mode
    <esc>       - Closes program

To run this you need to update the config files:

## Config Files
###### apiConfig.json - (requires updates)
    This holds all the information for calls to services to get the weather.
    API tokens needed:
      darksky.net - to get the actual weather (required)

###### clothingConfig.json - 
    Holds clothing options and conditions for the clothing
    items with no "gender" config apply to everyone, gender it completely optional.

###### peopleConfig.json - (requires updates) 
    Holds information for the people who you want to display clothing for
    Name - Their name to be displayed (Keep it short depending on the screen size of your display)
    Gender - works in conjunction with clothingConfig for items specifically for a gender - Not required
    Feel - "warm", "inbetween", "cool" - Adjusts clothes on how the person wishes to be 
        (i.e "cool" will add less and "warm" will add more clothes.)
  
###### tempAdjustConfig.json - 
    Holds the temp adjustment values for various conditions  

###### locationConfig - (requires updates)
    Holds location information to get your weather
    - Lat and Long to get the weather for the correct location
    - location name, this is the value that is displayed
