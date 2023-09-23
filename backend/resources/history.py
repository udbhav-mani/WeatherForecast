from datetime import datetime
import os
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests
from helpers.exceptions import WrongInputError
from helpers.response_parser import ResponseParser
from helpers.validators import Validators
from schemas import ForecastSchema

blp = Blueprint("Historical Data", "History", description="Operations on History")


@blp.route("/history/<string:city_name>")
class HistorytCity(MethodView):
    def get(self, city_name):
        if not Validators.validate_city_name(city_name=city_name):
            return {
                "error": {"code": 404, "message": "City name is invalid."},
                "status": "failure",
            }, 404
        try:
            date = request.args.get("date")
            # Validators.validate_days(days=days)
        except WrongInputError as error:
            return {
                "error": {"code": 404, "message": str(error)},
                "status": "failure",
            }, 404

        response_current = requests.get(
            os.getenv("RA_BASEURL_HISTORY"),
            params={"q": city_name, "dt": date},
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

        return ResponseParser.parse_history_respone(response=response_current)


@blp.route("/history")
class HistoryLatlong(MethodView):
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
            date = request.args.get("date")
            # Validators.validate_days(days=days)
        except WrongInputError as error:
            return {
                "error": {"code": 404, "message": str(error)},
                "status": "failure",
            }, 404

        response_current = requests.get(
            os.getenv("RA_BASEURL_HISTORY"),
            params={"q": f"{lat},{lon}", "dt": date},
            headers={
                "X-RapidAPI-Key": os.getenv("RA_APIKEY"),
                "X-RapidAPI-Host": os.getenv("RA_HOST"),
            },
        )
        return ResponseParser.parse_history_respone(response=response_current)
