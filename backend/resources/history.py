from datetime import datetime
import os
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests
from schemas import ForecastSchema

blp = Blueprint("Historical Data", "History", description="Operations on History")


@blp.route("/history")
class History(MethodView):
    @blp.response(200, ForecastSchema())
    def get(self):
        q = request.args.get("q")
        date = request.args.get("date")

        response_current = requests.get(
            os.getenv("RA_BASEURL_HISTORY"),
            params={"q": q, "dt": date},
            headers={
                "X-RapidAPI-Key": os.getenv("RA_APIKEY"),
                "X-RapidAPI-Host": os.getenv("RA_HOST"),
            },
        )

        if response_current.status_code != 200:
            abort(500, message=response_current.json()["error"]["message"])

        response_current = response_current.json()
        lat = response_current["location"]["lat"]
        lon = response_current["location"]["lon"]
        cityname = response_current["location"]["name"]

        day = response_current["forecast"]["forecastday"][0]
        temp = day["day"]["avgtemp_c"]
        temp_max = day["day"]["maxtemp_c"]
        temp_min = day["day"]["mintemp_c"]
        humidity = day["day"]["avghumidity"]
        date = datetime.fromtimestamp(day["date_epoch"])
        condition = day["day"]["condition"]["text"]

        return_dict = {
            "temp": temp,
            "max_temp": temp_max,
            "min_temp": temp_min,
            "humidity": humidity,
            "location": {
                "cityname": cityname,
                "lat": lat,
                "lon": lon,
                "localtime": date,
            },
            "condition": condition,
        }

        return return_dict
