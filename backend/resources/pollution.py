from datetime import datetime
import os
from flask import request
from flask.views import MethodView
import requests
from flask_smorest import Blueprint, abort
from schemas import PollutionSchema

blp = Blueprint("Pollution", "pollution", description="Operations on pollution")


@blp.route("/pollution")
class Pollution(MethodView):
    @blp.response(200, PollutionSchema())
    def get(self):
        args = request.args.get("q")
        lat, lon = args.split(",")
        response_current = requests.get(
            os.getenv("OWM_BASEURL_POLLUTION"),
            params={
                "lat": lat,
                "lon": lon,
                "appid": os.getenv("OWM_APIKEY"),
            },
        )

        if response_current.status_code != 200:
            abort(500, message=response_current.json()["message"])

        # return response_current.json()

        response_current = response_current.json()
        lat = response_current["coord"]["lat"]
        lon = response_current["coord"]["lon"]
        localtime = datetime.fromtimestamp(response_current["list"][0]["dt"])
        aqi = response_current["list"][0]["main"]["aqi"]
        pm25 = response_current["list"][0]["components"]["pm2_5"]
        pm10 = response_current["list"][0]["components"]["pm10"]
        so2 = response_current["list"][0]["components"]["so2"]
        no2 = response_current["list"][0]["components"]["no2"]
        co = response_current["list"][0]["components"]["co"]

        return_dict = {
            "location": {
                "lat": lat,
                "lon": lon,
                "localtime": localtime,
            },
            "aqi": aqi,
            "pm25": pm25,
            "pm10": pm10,
            "so2": so2,
            "no": no2,
            "co": co,
        }
        return return_dict
