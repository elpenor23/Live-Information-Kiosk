
from flask_restful import Resource
from flask import request
from managers.ClothingManager import ClothingManager

class ClothingResource(Resource):
    def get(self):
        
        if ("type" in request.args):
            type = request.args.get('type')
        else:
            # status HTTP_428_PRECONDITION_REQUIRED 
            return {"message": "type required"}, 428

        if type == "bodyparts":
            data = ClothingManager.get_bodyparts()

        elif type == "allclothes":
            data = ClothingManager.get_all_clothing()
            
        elif type == "calculate":
            error_ary = []
            if not ("feels" in request.args):
                error_ary.append("feels")

            if not ("genders" in request.args):
                error_ary.append("genders")

            if not ("names" in request.args):
                error_ary.append("names")

            if not ("ids" in request.args):
                error_ary.append("ids")

            if not ("colors" in request.args):
                error_ary.append("colors")
                
            if not ("lat" in request.args):
                error_ary.append("lat")

            if not ("lon" in request.args):
                error_ary.append("lon")

            if len(error_ary) > 0:
                comma = ","
                err_str = comma.join(error_ary)
                # status HTTP_428_PRECONDITION_REQUIRED
                return {"message": err_str + " required"}, 428  

            feels = request.args.get('feels')
            ids = request.args.get('ids')
            genders = request.args.get('genders')
            name = request.args.get('names')
            color = request.args.get('colors')
            lat = request.args.get('lat')
            lon = request.args.get('lon')

            data = ClothingManager.calculate_clothing(ids, feels, genders, name, color, lat, lon)

        else:
            # status HTTP_400_BAD_REQUEST 
            return {"message": "invaid type"}, 400    
        
        return data