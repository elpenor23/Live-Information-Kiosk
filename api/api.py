from flask import Flask
from flask_restful import Api
from resources.IndoorStatusResource import IndoorStatusResource
from resources.WeatherResource import WeatherResource
from database.database import db

app = Flask(__name__)

#SETUP Database
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////var/www/api/db/api.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/ericmalinowski/code/Live-Information-Kiosk/api/api.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
with app.app_context():
    db.create_all()

#SETUP API
api = Api = Api(app)
api.add_resource(IndoorStatusResource, "/indoor_status")
api.add_resource(WeatherResource, "/weather")
#Run the things
if __name__ == "__main__":
  app.run(host="10.0.0.6", port="5000", debug=True)
  #app.run()
