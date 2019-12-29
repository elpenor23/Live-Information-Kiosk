class FutureForecastDay(QFrame):
    def __init__(self, parent, weather=""):
        QFrame.__init__(self, parent, bg='black')

        icon_id = weather['icon']

        if icon_id in icon_lookup:
            icon = icon_lookup[icon_id]
        else:
            icon='assets/Sun.png'
            
        image = Image.open(icon)
        image = image.resize((50, 50), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)

        date_format = '%a %m/%d/%Y'
        dtenew = time.strftime(date_format, time.localtime(weather['time']))
        
        degree_sign= u'\N{DEGREE SIGN}'
        temp_format = "%s%s%s\n%s%s%s\n%s"
        
        temp = temp_format % ('High:', str(int(weather['apparentTemperatureHigh'])), degree_sign,
                              "Low:", str(int(weather['apparentTemperatureLow'])), degree_sign,
                              dtenew)
        
        #print(dtenew)
        
        self.eventName = temp
        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.eventNameLbl.pack(side=BOTTOM, anchor=N)