import os
import geocoder
import inquirer
from geopy.geocoders import Nominatim

from controllers import Weather
from controllers import Forecast
from controllers import Pollution
from controllers import History
from datetime import date, timedelta


class Entry:
    def entry(self):
        self.__choice_displayer()

    def __choice_displayer(self):
        choices = [
            inquirer.List(
                "choice",
                message="What do you want to know today?",
                choices=[
                    "Weather Currently",
                    "Weather Forecast",
                    "Weather History",
                    "Pollution",
                ],
            ),
        ]
        answers = inquirer.prompt(choices)
        choice = answers["choice"]

        data = self.__current_location()

        if choice == "Weather Currently":
            self.__current_weather_choices(data)

        elif choice == "Weather Forecast":
            self.__weather_forecast_choices(data)

        elif choice == "Weather History":
            self.__weather_history_choices(data)

        elif choice == "Pollution":
            self.__pollution_choices(data)

    def __current_weather_choices(self, data):
        weather = Weather()
        if len(data) == 1:
            weather.get_weather_by_city(cityname=data[0])
        else:
            weather.get_weather_by_latlon(lat=data[0], lon=data[1])

    def __weather_forecast_choices(self, data):
        choices = [
            inquirer.List(
                "choice",
                message="For how many days you want to see the forecast?",
                choices=["Next 1 Day", "Next 2 Days", "Next 3 Days"],
            ),
        ]
        answers = inquirer.prompt(choices)
        choice = answers["choice"]

        days = None
        if choice == "Next 1 Day":
            days = 1

        elif choice == "Next 2 Days":
            days = 2

        elif choice == "Next 3 Days":
            days = 3

        forecast = Forecast()
        if len(data) == 1:
            forecast.get_forecast_by_city(cityname=data[0], days=days)
        else:
            forecast.get_forecast_by_latlon(lat=data[0], lon=data[1], days=days)

    def __weather_history_choices(self, data):
        choices = [
            inquirer.List(
                "choice",
                message="Please select the date you want to see history for -> ",
                choices=[
                    (date.today() - timedelta(days=i)).__str__() for i in range(1, 6)
                ],
            ),
        ]
        answers = inquirer.prompt(choices)
        dt = answers["choice"]
        history = History()
        if len(data) == 1:
            history.get_history_by_city(cityname=data[0], date=dt)
        else:
            history.get_history_by_latlon(lat=data[0], lon=data[1], date=dt)

    def __pollution_choices(self, data):
        pollution = Pollution()
        if len(data) == 1:
            pollution.get_pollution_by_city(cityname=data[0])
        else:
            pollution.get_pollution_by_latlon(lat=data[0], lon=data[1])

    def __current_location(self):
        g = geocoder.ip("me")

        geoLoc = Nominatim(user_agent="MyAPP")
        lat, lon = g.latlng
        locname = geoLoc.reverse(f"{lat}, {lon}").__str__().split(",")[-3:]
        print(f"Your Current location is - {locname[0]},{locname[2]}")
        print(f"Latitude -> {lat}, Longitude -> {lon}.")
        choices = [
            inquirer.List(
                "choice",
                message="Do you want to continue with current coordinates?",
                choices=["Yes", "No"],
            ),
        ]
        answers = inquirer.prompt(choices)
        choice = answers["choice"]

        if choice == "Yes":
            return (lat, lon)

        elif choice == "No":
            return self.__city_or_latlong()

    def __city_or_latlong(self):
        os.system("cls")
        choices = [
            inquirer.List(
                "choice",
                message="What would you like to enter? ",
                choices=["Latitude-Longitude", "City Name"],
            ),
        ]

        answers = inquirer.prompt(choices)
        choice = answers["choice"]
        if choice == "Latitude-Longitude":
            lat = input("Please enter latitude -> ")
            lon = input("Please enter longitude -> ")

            return (lat, lon)

        elif choice == "City Name":
            cityname = input("Please enter city name -> ")
            return (cityname,)
