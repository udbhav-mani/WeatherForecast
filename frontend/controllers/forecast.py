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
            response = requests.get(self.FORECAST_URI, params={"q": cityname, "days": days})
            return response.json()
        except Exception as error:
            logger.error(f"get_forecast_by_city called with error : {error}")


    def get_forecast_by_latlon(self, lat=None, lon=None, days=None):
        logger.debug(f"get_forecast_by_latlon called with params: {lat}, {lon}, {days}")

        try:
            response = requests.get(
                self.FORECAST_URI, params={"q": f"{lat},{lon}", "days": days}
            )
            return response.json()
        except Exception as error:
            logger.error(f"get_forecast_by_latlon called with error : {error}")
            

if __name__ == "__main__":
    obj = Forecast()
    obj.get_forecast_by_city(cityname="new york", days=3)
