import os
import requests


class Weather:
    def get_weather_by_city(self, cityname=None):
        WEATHER_URI_CITY = "http://127.0.0.1:5000/weather/city"
        response = requests.get(WEATHER_URI_CITY, params={"q": cityname})
        print(response.json())

    def get_weather_by_latlon(self, lat=None, lon=None):        
        WEATHER_URI_LATLON = "http://127.0.0.1:5000/weather/latlon"
        response = requests.get(WEATHER_URI_LATLON, params={"q": f"{lat},{lon}"})
        print(response.json())


if __name__ == "__main__":
    obj = Weather()
    obj.get_weather_by_latlon(cityname="new york")

