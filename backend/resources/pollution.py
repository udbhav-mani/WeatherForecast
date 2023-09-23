from datetime import datetime
import os
from flask import request
from flask.views import MethodView
import requests
from flask_smorest import Blueprint, abort
from helpers.response_parser import ResponseParser
from helpers.exceptions import WrongInputError
from helpers.validators import Validators
from geopy.geocoders import Nominatim

blp = Blueprint("Pollution", "pollution", description="Operations on pollution")


@blp.route("/pollution")
class Pollution(MethodView):
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

        response_current = requests.get(
            os.getenv("OWM_BASEURL_POLLUTION"),
            params={
                "lat": lat,
                "lon": lon,
                "appid": os.getenv("OWM_APIKEY"),
            },
        )
        if response_current.status_code != 200:
            error_message = response_current.json()["message"]
            return {
                "error": {"code": 500, "message": error_message},
                "status": "failure",
            }, 500

        return ResponseParser.parse_pollution_response(response_current)


@blp.route("/pollution/<string:city_name>")
class PollutionCity(MethodView):
    def get(self, city_name):
        if not Validators.validate_city_name(city_name=city_name):
            return {
                "error": {"code": 404, "message": "City name is invalid."},
                "status": "failure",
            }, 404

        try:
            geolocator = Nominatim(user_agent="MyApp")
            location = geolocator.geocode(city_name)
            if location is None:
                return {
                    "error": {"code": 404, "message": "Location not found."},
                    "status": "failure",
                }, 404

            lat = location.latitude
            lon = location.longitude

        except Exception as error:
            return {
                "error": {"code": 404, "message": str(error)},
                "status": "failure",
            }, 404
        else:
            response_current = requests.get(
                os.getenv("OWM_BASEURL_POLLUTION"),
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": os.getenv("OWM_APIKEY"),
                },
            )
            if response_current.status_code != 200:
                error_message = response_current.json()["message"]
                return {
                    "error": {"code": 500, "message": error_message},
                    "status": "failure",
                }, 500

            return ResponseParser.parse_pollution_response(response_current)
