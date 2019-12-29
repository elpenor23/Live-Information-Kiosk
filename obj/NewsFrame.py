class News(QFrame):
    def __init__(self, parent, *args, **kwargs):
        QFrame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'News' # 'News' is more internationally generic
        self.newsLbl = QLabel(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.newsLbl.pack(side=TOP, anchor=W)
        self.headlinesContainer = QFrame(self, bg="black")
        self.headlinesContainer.pack(side=TOP)
        self.get_headlines()

    def get_headlines(self):
        # remove all children
        for widget in self.headlinesContainer.winfo_children():
            widget.destroy()
        
        feed = get_news(news_country_code)

        if feed is not None:
            for post in feed.entries[0:5]:
                headline = NewsHeadline(self.headlinesContainer, post.title)
                headline.pack(side=TOP, anchor=W)
    
        self.after(600000, self.get_headlines)