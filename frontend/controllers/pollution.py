import requests
from geopy.geocoders import Nominatim
from pprint import pprint
import logging

logger = logging.getLogger(__name__)


class Pollution:
    POLLUTION_URI = "http://127.0.0.1:5000/pollution"

    def get_pollution_by_city(self, cityname=None):
        logger.debug(f"get_pollution_by_city called with params: {cityname}")

        response = requests.get(self.POLLUTION_URI + f"/{cityname}")

        if response.status_code == 500 or response.status_code == 404:
            error = response.json().get("error").get("message")
            logger.error(f"get_pollution_by_city called with error : {error}")
            return {
                "status": "failure",
                "error": {"code": 500, "message": error},
            }
        else:
            return response.json()

    def get_pollution_by_latlon(self, lat=None, lon=None):
        logger.debug(f"get_pollution_by_latlon called with params: {lat}, {lon}")
        response = requests.get(
            self.POLLUTION_URI,
            params={"lat": f"{lat}", "lon": f"{lon}"},
        )
        if response.status_code == 500 or response.status_code == 404:
            error = response.json().get("error").get("message")
            logger.error(f"get_pollution_by_latlon called with error : {error}")
            return {
                "status": "failure",
                "error": {"code": 500, "message": error},
            }
        else:
            return response.json()
