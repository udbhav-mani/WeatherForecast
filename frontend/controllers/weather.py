import os
from pprint import pprint
import requests
import logging

logger = logging.getLogger(__name__)


class Weather:
    def get_weather_by_city(self, cityname=None):
        logger.debug(f"get_weather_by_city called with params: {cityname}")
        WEATHER_URI_CITY = f"http://127.0.0.1:5000/weather/{cityname}"
        response = requests.get(WEATHER_URI_CITY)

        if response.status_code == 500 or response.status_code == 404:
            error = response.json().get("error").get("message")
            logger.error(f"get_weather_by_city called with error : {error}")
            return {
                "status": "failure",
                "error": {"code": 500, "message": error},
            }
        else:
            return response.json()

    def get_weather_by_latlon(self, lat=None, lon=None):
        logger.debug(f"get_weather_by_latlon called with params: {lat}, {lon}")
        WEATHER_URI_LATLON = "http://127.0.0.1:5000/weather"
        response = requests.get(
            WEATHER_URI_LATLON, params={"lat": f"{lat}", "lon": f"{lon}"}
        )
        if response.status_code == 500 or response.status_code == 404:
            error = response.json().get("error").get("message")
            logger.error(f"get_weather_by_latlon called with error : {error}")
            return {
                "status": "failure",
                "error": {"code": 500, "message": error},
            }
        else:
            return response.json()
