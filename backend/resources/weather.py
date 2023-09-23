from datetime import datetime
import os
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests
from helpers.exceptions import WrongInputError
from helpers.response_parser import ResponseParser
from helpers.validators import Validators
from schemas import WeatherSchema

blp = Blueprint("Weather", "Weather", description="Operations on weather")


@blp.route("/weather/<string:city_name>")
class Weather(MethodView):
    def get(self, city_name):
        if not Validators.validate_city_name(city_name=city_name):
            return {
                "error": {"code": 400, "message": "City name is invalid."},
                "status": "failure",
            }, 400

        response_current = requests.get(
            os.getenv("OWM_BASEURL_WEATHER"),
            params={
                "q": city_name,
                "units": "metric",
                "appid": os.getenv("OWM_APIKEY"),
            },
        )
        if response_current.status_code != 200:
            error_message = response_current.json()["message"]
            return {
                "error": {"code": 500, "message": error_message},
                "status": "failure",
            }, 500

        return ResponseParser.parse_weather_response(response_current)


@blp.route("/weather")
class Weather(MethodView):
    def get(self):
        try:
            lat = request.args.get("lat")
            lon = request.args.get("lon")
            Validators.validate_latlong(lat=lat, lon=lon)
        except WrongInputError as error:
            return {
                "error": {"code": 400, "message": str(error)},
                "status": "failure",
            }, 400

        response_current = requests.get(
            os.getenv("OWM_BASEURL_WEATHER"),
            params={
                "lat": lat,
                "lon": lon,
                "units": "metric",
                "appid": os.getenv("OWM_APIKEY"),
            },
        )
        if response_current.status_code != 200:
            error_message = response_current.json()["message"]
            return {
                "error": {"code": 500, "message": error_message},
                "status": "failure",
            }, 500

        return ResponseParser.parse_weather_response(response_current)
