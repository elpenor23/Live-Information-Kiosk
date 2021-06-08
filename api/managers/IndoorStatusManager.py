
from database.database import db
from database.StatusModel import StatusModel
from managers.ErrorManager import ErrorManager
from datetime import datetime


DATE_FORMAT = "%m/%d/%Y %H:%M:%S"
MINUTES_TO_ADD = 0 #FOR FUTURE USE IN LATCHING

class IndoorStatusManager():
    def setup_db():
        statuses = StatusModel.query.all()
        status_count = len(statuses)

        if status_count == 0:
            new_status = StatusModel(data = "XX", last_set = datetime.now(), number_of_calls = 0, average_seconds_between_calls = 0)
            db.session.add(new_status)
            db.session.commit()

    def get_status():
        try:
            statuses = StatusModel.query.all()
            status = statuses[0]
            return_message = {
                "data": status.data, 
                "last_set": status.last_set.strftime(DATE_FORMAT)
                }, 200
        except Exception as err:
            ErrorManager.log_error("IndoorStatusManager.get_status: " + str(err))
            return_message = {"error": "Error getting Indoor Status from DB"}, 500

        return return_message

    def get_checkup_data():
        try:
            statuses = StatusModel.query.all()
            status = statuses[0]
            return_message = {
                "last_set": status.last_set.strftime(DATE_FORMAT),
                "number_of_calls": status.number_of_calls,
                "average_seconds_between_calls": status.average_seconds_between_calls
                }
        except Exception as err:
            ErrorManager.log_error("IndoorStatusManager.get_checkup_data: " + str(err))
            return_message = {"error": "Error getting Indoor Status from DB" + str(err)}

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
            local_last_set = status.last_set

            status.data = data
            status.average_seconds_between_calls = int(
                    ((current_time - local_last_set).total_seconds() + (status.average_seconds_between_calls * status.number_of_calls)) / (status.number_of_calls + 1)
                )
            status.last_set = current_time
            status.number_of_calls += 1
            
            db.session.commit()

            return_message = {"message": "Success!"}, 200
        except Exception as err:
            ErrorManager.log_error("IndoorStatusManager.set_status: " + str(err))
            return_message = {"error": f"Error saving status: {err}"}, 500

        
        return return_message