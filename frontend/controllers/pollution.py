import requests
from geopy.geocoders import Nominatim
from pprint import pprint
import logging

logger = logging.getLogger(__name__)


class Pollution:
    POLLUTION_URI = "http://127.0.0.1:5000/pollution"

    def get_pollution_by_city(self, cityname=None):
        logger.debug(f"get_pollution_by_city called with params: {cityname}")

        try:
            geolocator = Nominatim(user_agent="MyApp")
            location = geolocator.geocode(cityname)
            if location is None:
                raise Exception("Location Not found!! ")

            response = requests.get(
                self.POLLUTION_URI,
                params={"q": f"{location.latitude},{location.longitude}"},
            )

            if response.status_code != 500:
                return response.json()

            else:
                raise Exception(response.json()["message"])

        except Exception as error:
            logger.error(f"get_pollution_by_city called with error : {error}")
            return error.__str__()

    def get_pollution_by_latlon(self, lat=None, lon=None):
        logger.debug(f"get_pollution_by_latlon called with params: {lat}, {lon}")
        try:
            response = requests.get(self.POLLUTION_URI, params={"q": f"{lat},{lon}"})

            if response.status_code != 500:
                return response.json()

            else:
                raise Exception(response.json()["message"])
        except Exception as error:
            logger.error(f"get_pollution_by_latlon called with error : {error}")
            return error.__str__()


if __name__ == "__main__":
    obj = Pollution()
    obj.get_pollution_by_city(cityname="delhi")
