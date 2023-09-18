import os
import requests


class History:
    HISTORY_URI = "http://127.0.0.1:5000/history"

    def get_history_by_city(self, cityname=None, date=None):
        response = requests.get(self.HISTORY_URI, params={"q": cityname, "date": date})
        return response.json()

    def get_history_by_latlon(self, lat=None, lon=None, date=None):
        response = requests.get(
            self.HISTORY_URI, params={"q": f"{lat},{lon}", "date": date}
        )
        return response.json()


if __name__ == "__main__":
    obj = History()
    obj.get_history_by_city(cityname="new york", date="2023-09-15")
