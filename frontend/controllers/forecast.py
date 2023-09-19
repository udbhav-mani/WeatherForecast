import os
from pprint import pprint
import requests
import logging

logger = logging.getLogger(__name__)


class Forecast:
    FORECAST_URI = "http://127.0.0.1:5000/forecast"

    def get_forecast_by_city(self, cityname=None, days=None):
        logger.debug(f"get_forecast_by_city called with params: {cityname}, {days}")

        try:
            response = requests.get(
                self.FORECAST_URI, params={"q": cityname, "days": days}
            )
            if response.status_code != 500:
                return response.json()

            else:
                raise Exception(response.json()["message"])
        except Exception as error:
            logger.error(f"get_forecast_by_city called with error : {error}")
            return error.__str__()

    def get_forecast_by_latlon(self, lat=None, lon=None, days=None):
        logger.debug(f"get_forecast_by_latlon called with params: {lat}, {lon}, {days}")

        try:
            response = requests.get(
                self.FORECAST_URI, params={"q": f"{lat},{lon}", "days": days}
            )

            if response.status_code != 500:
                return response.json()

            else:
                raise Exception(response.json()["message"])
        except Exception as error:
            logger.error(f"get_forecast_by_latlon called with error : {error}")
            return error.__str__()


if __name__ == "__main__":
    obj = Forecast()
    print(obj.get_forecast_by_latlon(lat=0.0, lon=0.0, days=3))
