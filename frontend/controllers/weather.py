import requests


class Weather:
    def get_weather_by_city(self, cityname=None):
        uri = f"http://127.0.0.1:5000/weather/city"
        response = requests.get(uri, params={"q": cityname})
        print(response.json())

    def get_weather_by_latlon(self, lat=None, lon=None):
        uri = f"http://127.0.0.1:5000/weather/latlon"
        response = requests.get(uri, params={"q": f"{lat},{lon}"})
        print(response.json())


if __name__ == "__main__":
    obj = Weather()
    obj.get_weather_by_city(cityname="new york")
