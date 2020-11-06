
from database.database import db
from database.StatusModel import StatusModel
from managers.ErrorManager import ErrorManager
from datetime import datetime


DATE_FORMAT = "%m/%d/%Y, %H:%M:%S"
MINUTES_TO_ADD = 0

class IndoorStatusManager():
    def setup_db():
        new_status = StatusModel(data = "XX", last_set = datetime.now())
        db.session.add(new_status)
        db.session.commit()

    def get_status():
        try:
            statuses = StatusModel.query.all()
            status = statuses[0]
            return_message = {"data": status.data, "last_set": status.last_set.strftime(DATE_FORMAT)}, 200
        except Exception as err:
            ErrorManager.log_error("IndoorStatusManager.get_status: " + err)
            return_message = {"error": "Error getting Indoor Status from DB"}, 500

        return return_message

    def set_status(data):
        try:
            statuses = StatusModel.query.all()
            status = statuses[0]
            current_time = datetime.now()
            # This is for latching not sure if we need it so commenting it out
            # #if we are unsetting the latch we need to make sure that it has been
            # # at least 2 minutes since the last set
            # if set == 0:
            #   if record.is_set == 1:
            #     #we are trying to unset the latch
            #     deadline_date = record.last_set + timedelta(minutes = MINUTES_TO_ADD)
            #     if current_time < deadline_date:
            #       return

            status.data = data
            status.last_set = current_time
            db.session.commit()

            return_message = {"message": "Success!"}, 200
        except Exception as err:
            ErrorManager.log_error("IndoorStatusManager.set_status: " + err)
            return_message = {"error": f"Error saving status: {err}"}, 500

        
        return return_message