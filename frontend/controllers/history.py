import os
import requests
import logging

logger = logging.getLogger(__name__)


class History:
    HISTORY_URI = "http://127.0.0.1:5000/history"

    def get_history_by_city(self, cityname=None, date=None):
        logger.debug(f"get_history_by_city called with params: {cityname}, {date}")
        try:
            response = requests.get(
                self.HISTORY_URI, params={"q": cityname, "date": date}
            )
            if response.status_code != 500:
                return response.json()
            else:
                raise Exception(response.json()["message"])
        except Exception as error:
            logger.error(f"get_history_by_city called with error : {error}")
            return error.__str__()

    def get_history_by_latlon(self, lat=None, lon=None, date=None):
        logger.debug(f"get_history_by_city called with params: {lat}, {lon}, {date}")
        try:
            response = requests.get(
                self.HISTORY_URI, params={"q": f"{lat},{lon}", "date": date}
            )
            if response.status_code != 500:
                return response.json()

            else:
                raise Exception(response.json()["message"])
        except Exception as error:
            logger.error(f"get_history_by_latlon called with error : {error}")
            return error.__str__()


if __name__ == "__main__":
    obj = History()
    obj.get_history_by_city(cityname="new york", date="2023-09-15")
