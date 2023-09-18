import requests
from geopy.geocoders import Nominatim


class POLLUTION:
    POLLUTION_URI = "http://127.0.0.1:5000/pollution"

    def get_pollution_by_city(self, cityname=None):
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(cityname)
        response = requests.get(
            self.POLLUTION_URI,
            params={"q": f"{location.latitude},{location.longitude}"},
        )
        print(response.json())

    def get_pollution_by_latlon(self, lat=None, lon=None):
        response = requests.get(self.POLLUTION_URI, params={"q": f"{lat},{lon}"})
        print(response.json())


if __name__ == "__main__":
    obj = POLLUTION()
    obj.get_pollution_by_city(cityname="delhi")
