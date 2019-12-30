# RunnerClothing
What to wear while running based on weather and person

To run this you need to update the config files:

*apiConfig.json - This holds all the information for calls to services to get the weather, your location (beta) and news.
  API tokens needed:
    darksky.net - to get the actual weather (required)
    ipstack.com - to get your location based on IP (optional)

clothingConfig.json - Holds clothing options and conditions for the clothing

*peopleConfig.json - Holds information for the people who you want to display clothing for
  Name - Their name to be displayed (Keep iot short depending on the screen size of your display)
  Gender - "man" or "woman" (does not actually do anything but it is set up to be able to.
  Feel - "warm", "inbetween", "cool" - Adjusts clothes on how the person wishes to be (i.e "cool" will add less and "warm" will add more clothes.
  
tempAdjustConfig.json - Holds the temp adjustment values for various conditions  

*locationConfig - Holds location information to get your weather

(*) - Requires Updates
