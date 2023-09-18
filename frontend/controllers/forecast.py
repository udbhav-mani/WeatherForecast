import os
from pprint import pprint
import requests


class Forecast:
    FORECAST_URI = "http://127.0.0.1:5000/forecast"

    def get_forecast_by_city(self, cityname=None, days=None):
        response = requests.get(self.FORECAST_URI, params={"q": cityname, "days": days})
        return response.json()

    def get_forecast_by_latlon(self, lat=None, lon=None, days=None):
        response = requests.get(
            self.FORECAST_URI, params={"q": f"{lat},{lon}", "days": days}
        )
        return response.json()


if __name__ == "__main__":
    obj = Forecast()
    obj.get_forecast_by_city(cityname="new york", days=3)
