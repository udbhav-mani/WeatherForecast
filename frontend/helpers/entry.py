import os
import geocoder
import inquirer
from geopy.geocoders import Nominatim
from controllers import Weather, Forecast, Pollution, History
from datetime import date, timedelta
import pyfiglet
import time
import os
from yaspin import yaspin
from termcolor import colored

from prettytable import PrettyTable, ALL
from utils import prompts
from utils import choices

from helpers.validators import Validators


class Entry:
    def entry(self):
        os.system
        font = pyfiglet.Figlet(font="graffiti")
        text = font.renderText("Weather Forecaster")
        colored_text = colored(text, color="cyan")
        print(colored_text, end="")

        self.__horizontal_loading_bar()
        self.__clear_terminal()
        self.__choice_displayer()

    def __choice_displayer(self):
        prompt = prompts.INITIAL_PROMPT
        options = choices.INITIAL_CHOICES
        choice = self.__get_choice(prompt=prompt, options=options)

        if choice == "Exit":
            self.__end_program()
            return

        data = self.__current_location()
        if data is None:
            return

        if choice == "Weather Currently":
            self.__current_weather_choices(data)

        elif choice == "Weather Forecast":
            self.__weather_forecast_choices(data)

        elif choice == "Weather History":
            self.__weather_history_choices(data)

        elif choice == "Pollution":
            self.__pollution_choices(data)

        self.__choose_to_continue()

    def __current_weather_choices(self, data):
        weather = Weather()
        if len(data) == 1:
            data = weather.get_weather_by_city(cityname=data[0])
        else:
            data = weather.get_weather_by_latlon(lat=data[0], lon=data[1])

        if isinstance(data, str):
            print(data.title())
            return

        table = self.__dictionary_to_table(data)
        print(table)

    def __weather_forecast_choices(self, data):
        prompt = prompts.WEATHER_FORECAST_PROMPT
        options = choices.WEATHER_FORECAST_CHOICES
        choice = self.__get_choice(prompt=prompt, options=options)

        days = None
        if choice == "Next 1 Day":
            days = 1

        elif choice == "Next 2 Days":
            days = 2

        elif choice == "Next 3 Days":
            days = 3

        forecast = Forecast()
        if len(data) == 1:
            data = forecast.get_forecast_by_city(cityname=data[0], days=days)
        else:
            data = forecast.get_forecast_by_latlon(lat=data[0], lon=data[1], days=days)

        if isinstance(data, str):
            print(data)
            return

        for item in data:
            table = self.__dictionary_to_table(item)
            print(table)
            print("\n\n")

    def __weather_history_choices(self, data):
        prompt = prompts.WEATHER_HISTORY_PROMPT
        options = choices.WEATHER_HISTORY_CHOICES
        dt = self.__get_choice(prompt=prompt, options=options)

        history = History()
        if len(data) == 1:
            data = history.get_history_by_city(cityname=data[0], date=dt)
        else:
            data = history.get_history_by_latlon(lat=data[0], lon=data[1], date=dt)

        if isinstance(data, str):
            print(data)
            return

        table = self.__dictionary_to_table(data)
        print(table)

    def __pollution_choices(self, data):
        pollution = Pollution()
        if len(data) == 1:
            data = pollution.get_pollution_by_city(cityname=data[0])
        else:
            data = pollution.get_pollution_by_latlon(lat=data[0], lon=data[1])

        if isinstance(data, str):
            print(data.title())
            return

        table = self.__dictionary_to_table(data)
        print(table)

    def __current_location(self):
        try:
            g = geocoder.ip("me")
            geoLoc = Nominatim(user_agent="MyAPP")
            lat, lon = g.latlng
            locname = geoLoc.reverse(f"{lat}, {lon}").__str__().split(",")[-3:]
        except Exception:
            print("Could not get current location!! PLease restart and try!!")
            return None
        else:
            print(f"Your Current location is - {locname[0]},{locname[2]}")
            print(f"Latitude -> {lat}, Longitude -> {lon}.")

            prompt = prompts.CURRENT_LOCATION_PROMPT
            options = choices.CURRENT_LOCATION_CHOICES
            choice = self.__get_choice(prompt=prompt, options=options)

            if choice == "Yes":
                return (lat, lon)

            elif choice == "No":
                return self.__city_or_latlong()

    def __city_or_latlong(self):
        os.system("cls")

        prompt = prompts.LAT_OR_LONG_PROMPT
        options = choices.LAT_OR_LONG_CHOICES
        choice = self.__get_choice(prompt=prompt, options=options)

        if choice == "Latitude-Longitude":
            lat = None
            lon = None
            while True:
                try:
                    lat = float(input("Please enter latitude -> "))
                    break
                except ValueError:
                    print("Please give correct input.")
            while True:
                try:
                    lon = float(input("Please enter longitude -> "))
                    break
                except ValueError:
                    print("Please give correct input.")

            return (lat, lon)

        elif choice == "City Name":
            cityname = GetInput.get_city_name()
            return (cityname,)

    def __horizontal_loading_bar(self):
        with yaspin(text="Loading...", color="yellow") as sp:
            for i in range(101):
                progress = "=" * i
                sp.text = f"Loading... [{progress:<100}] {i}%"
                sp.show()
                time.sleep(0.03)
            sp.text = "Loading... [====================================================================================================] 100%"
            sp.ok("✔")

    def __clear_terminal(self):
        os.system("cls" if os.name == "nt" else "clear")

    def __end_program(self):
        os.system("cls")
        font = pyfiglet.Figlet(font="graffiti")
        text = font.renderText("Thank You")
        colored_text = colored(text, color="cyan")
        print(colored_text, end="")
        time.sleep(3)
        os.system("cls")
        quit()

    def __choose_to_continue(self):
        prompt = prompts.CHOOSE_CONTINUE_PROMPT
        options = choices.CHOOSE_CONTINUE_CHOICES
        choice = self.__get_choice(prompt=prompt, options=options)

        os.system("cls")
        if choice == "Yes":
            self.__choice_displayer()
        elif choice == "No":
            self.__end_program()

    def __dictionary_to_table(self, data):
        table = PrettyTable()
        table.hrules = ALL
        table.field_names = ["Property", "Value"]
        for key, value in data.items():
            if isinstance(value, dict):
                nested_table = self.__dictionary_to_table(value)
                table.add_row([colored(key, "cyan"), nested_table])
            else:
                colored_key = colored(key, "cyan")
                colored_value = colored(str(value), "green")
                table.add_row([colored_key, colored_value])
        return table

    def __get_choice(self, prompt, options):
        choices = [
            inquirer.List("choice", message=prompt, choices=options),
        ]
        answers = inquirer.prompt(choices)
        return answers["choice"]


class GetInput:
    """
    class to group all input methods
    The associated methods also validate input
    """

    @staticmethod
    def get_city_name():
        """validates cityname according to regex = [A-Za-z ]+"""
        cityname = input("Enter cityname - ")
        if not Validators.validate_input(cityname):
            print("Invalid cityname!! Try again!")
            cityname = GetInput.get_city_name()

        return cityname
