class FutureForecast(QFrame):
    def __init__(self, parent, *args, **kwargs):
        QFrame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'Future Forcast' 
        self.daysLbl = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.daysLbl.pack(side=TOP, anchor=W)
        self.dayContainer = QFrame(self, bg="black")
        self.dayContainer.pack(side=LEFT)
        self.get_days()

    def get_days(self):
        
        #remove old data first
        for widget in self.dayContainer.winfo_children():
            widget.destroy()
        
        if latitude is None and longitude is None:
            loc = get_location()
            lat = loc['lat']
            lon = loc['lon']
            loclbl = loc['location']
        else:
            lat = latitude
            lon = longitude
            loclbl = location
        
        weather_obj = get_weather(lat, lon)
        
        i=1
        for day_weather in weather_obj['daily']['data']:
            weather_date = time.strftime('%m/%d/%Y', time.localtime(day_weather['time']))
            current_date = datetime.datetime.today().strftime('%m/%d/%Y')
            
            #print(weather_date)
            #print(current_date)
            
            if weather_date > current_date and i <= max_days:
                day = FutureForecastDay(self.dayContainer, day_weather)
                day.pack(side=LEFT, anchor=W)
                i += 1
    
        self.after(600000, self.get_days)