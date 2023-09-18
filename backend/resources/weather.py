from datetime import datetime
import os
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests
from schemas import WeatherSchema

blp = Blueprint("Weather", "Weather", description="Operations on weather")


@blp.route("/weather/<string:mode>")
class Weather(MethodView):
    @blp.response(200, WeatherSchema())
    def get(self, mode):
        if mode not in ["city", "latlon"]:
            abort(400, message="Invalid parameter! Choose between city and latlong")

        args = request.args.get("q")

        if mode == "city":
            response_current = requests.get(
                os.getenv("OWM_BASEURL_WEATHER"),
                params={
                    "q": args,
                    "units": "metric",
                    "appid": os.getenv("OWM_APIKEY"),
                },
            )
        else:
            lat, lon = args.split(",")
            response_current = requests.get(
                os.getenv("OWM_BASEURL_WEATHER"),
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": os.getenv("OWM_APIKEY"),
                    "units": "metric",
                },
            )

        if response_current.status_code != 200:
            abort(500, message=response_current.json()["message"])

        response_current = response_current.json()
        temp = response_current["main"]["temp"]
        temp_max = response_current["main"]["temp_max"]
        temp_min = response_current["main"]["temp_min"]
        feels_like = response_current["main"]["feels_like"]
        humidity = response_current["main"]["humidity"]
        pressure = response_current["main"]["pressure"]
        sunrise = datetime.fromtimestamp(response_current["sys"]["sunrise"])
        sunset = datetime.fromtimestamp(response_current["sys"]["sunset"])
        localtime = datetime.fromtimestamp(response_current["dt"])
        lat = response_current["coord"]["lat"]
        lon = response_current["coord"]["lon"]
        cityname = response_current["name"]

        return_dict = {
            "temp": temp,
            "max_temp": temp_max,
            "min_temp": temp_min,
            "feels_like": feels_like,
            "pressure": pressure,
            "humidity": humidity,
            "astro": {"sunrise": sunrise, "sunset": sunset},
            "location": {
                "cityname": cityname,
                "lat": lat,
                "lon": lon,
                "localtime": localtime,
            },
        }
        return return_dict
