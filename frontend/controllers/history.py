import os
import requests
import logging

logger = logging.getLogger(__name__)


class History:
    HISTORY_URI = "http://127.0.0.1:5000/history"

    def get_history_by_city(self, cityname=None, date=None):
        logger.debug(f"get_history_by_city called with params: {cityname}, {date}")

        response = requests.get(
            self.HISTORY_URI + f"/{cityname}", params={"date": date}
        )
        if response.status_code == 500 or response.status_code == 404:
            error = response.json().get("error").get("message")
            logger.error(f"get_history_by_city called with error : {error}")
            return {
                "status": "failure",
                "error": {"code": 500, "message": error},
            }
        else:
            return response.json()

    def get_history_by_latlon(self, lat=None, lon=None, date=None):
        logger.debug(f"get_history_by_latlon called with params: {lat}, {lon}, {date}")

        response = requests.get(
            self.HISTORY_URI,
            params={"lat": f"{lat}", "lon": f"{lon}", "date": date},
        )
        if response.status_code == 500 or response.status_code == 404:
            error = response.json().get("error").get("message")
            logger.error(f"get_history_by_latlon called with error : {error}")
            return {
                "status": "failure",
                "error": {"code": 500, "message": error},
            }
        else:
            return response.json()


if __name__ == "__main__":
    obj = History()
    obj.get_history_by_city(cityname="new york", date="2023-09-15")
