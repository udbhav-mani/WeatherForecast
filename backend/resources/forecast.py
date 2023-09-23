import os
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import requests
from helpers.response_parser import ResponseParser
from helpers.exceptions import WrongInputError
from helpers.validators import Validators

blp = Blueprint("Forecast", "Forecast", description="Operations on Forecast")


@blp.route("/forecast/<string:city_name>")
class ForecastCity(MethodView):
    def get(self, city_name):
        if not Validators.validate_city_name(city_name=city_name):
            return {
                "error": {"code": 404, "message": "City name is invalid."},
                "status": "failure",
            }, 404
        try:
            days = request.args.get("days")
            Validators.validate_days(days=days)
        except WrongInputError as error:
            return {
                "error": {"code": 404, "message": str(error)},
                "status": "failure",
            }, 404

        response_current = requests.get(
            os.getenv("RA_BASEURL_FORECAST"),
            params={"q": city_name, "days": days},
            headers={
                "X-RapidAPI-Key": os.getenv("RA_APIKEY"),
                "X-RapidAPI-Host": os.getenv("RA_HOST"),
            },
        )

        if response_current.status_code != 200:
            error_message = response_current.json()["error"]["message"]
            return {
                "error": {"code": 500, "message": error_message},
                "status": "failure",
            }, 500

        return ResponseParser.parse_forecast_response(response=response_current)


@blp.route("/forecast")
class ForecastLatlong(MethodView):
    def get(self):
        try:
            lat = request.args.get("lat")
            lon = request.args.get("lon")
            Validators.validate_latlong(lat=lat, lon=lon)
        except WrongInputError as error:
            return {
                "error": {"code": 404, "message": str(error)},
                "status": "failure",
            }, 404

        try:
            days = request.args.get("days")
            Validators.validate_days(days=days)
        except WrongInputError as error:
            return {
                "error": {"code": 404, "message": str(error)},
                "status": "failure",
            }, 404

        response_current = requests.get(
            os.getenv("RA_BASEURL_FORECAST"),
            params={"q": f"{lat},{lon}", "days": days},
            headers={
                "X-RapidAPI-Key": os.getenv("RA_APIKEY"),
                "X-RapidAPI-Host": os.getenv("RA_HOST"),
            },
        )
        return ResponseParser.parse_forecast_response(response=response_current)
