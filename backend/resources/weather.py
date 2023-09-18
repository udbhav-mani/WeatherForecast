from datetime import datetime
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests
from schemas import LocationSchema
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
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": args,
                    "units": "metric",
                    "appid": "df57d20422fed2e720c2fae8fa4c9777",
                },
            )
        else:
            lat, lon = args.split(",")
            response_current = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": "df57d20422fed2e720c2fae8fa4c9777",
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
