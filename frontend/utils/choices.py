from datetime import date, timedelta

INITIAL_CHOICES = [
    "Weather Currently",
    "Weather Forecast",
    "Weather History",
    "Pollution",
    "Exit",
]
WEATHER_FORECAST_CHOICES = ["Next 1 Day", "Next 2 Days", "Next 3 Days"]
WEATHER_HISTORY_CHOICES = [
    (date.today() - timedelta(days=i)).__str__() for i in range(1, 6)
]
CURRENT_LOCATION_CHOICES = ["Yes", "No"]
LAT_OR_LONG_CHOICES = ["Latitude-Longitude", "City Name"]
CHOOSE_CONTINUE_CHOICES = ["Yes", "No"]
