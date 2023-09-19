from datetime import datetime
import os
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests
from schemas import ForecastSchema

blp = Blueprint("Forecast", "Forecast", description="Operations on Forecast")


@blp.route("/forecast")
class Forecast(MethodView):
    @blp.response(200, ForecastSchema(many=True))
    def get(self):
        q = request.args.get("q")
        days = request.args.get("days")

        response_current = requests.get(
            os.getenv("RA_BASEURL_FORECAST"),
            params={"q": q, "days": days},
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

        ans = []

        forecast_days = response_current["forecast"]["forecastday"]
        for day in forecast_days:
            temp = day["day"]["avgtemp_c"]
            temp_max = day["day"]["maxtemp_c"]
            temp_min = day["day"]["mintemp_c"]
            humidity = day["day"]["avghumidity"]
            date = datetime.fromtimestamp(day["date_epoch"])
            chance_of_rain = day["day"]["daily_will_it_rain"]
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
                "chance_of_rain": chance_of_rain,
                "condition": condition,
            }
            ans.append(return_dict)

        return ans
