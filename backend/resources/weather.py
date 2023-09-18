from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests
from schemas import LocationSchema
from schemas import WeatherSchema

blp = Blueprint("Weather", "Weather", description="Operations on weather")


@blp.route("/weather/<string:mode>")
class Weather(MethodView):
    # @blp.response(200, WeatherSchema)
    def get(self, mode):
        if mode not in ["city", "latlon"]:
            abort(400, message="Invalid parameter! Choose between city and latlong")

        args = request.args.get("q")
        if mode == "city":
            response_current = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": args, "appid": "df57d20422fed2e720c2fae8fa4c9777"},
            )
            return response_current.json()

        # ?lat=44.34&lon=10.99&appid=df57d20422fed2e720c2fae8fa4c9777&units=metric

        # data = response_current.json()
        # temp_c = data["current"]["temp_c"]
        # temp_f = data["current"]["temp_f"]
        # max_temp = data["current"]["temp_f"]
        # return {"gv": temp_c}

    @blp.arguments(LocationSchema)
    @blp.response(201, WeatherSchema)
    def post(self, item_data):
        pass
