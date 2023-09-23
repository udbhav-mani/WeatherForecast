import re

from helpers.exceptions import WrongInputError


class Validators:
    @staticmethod
    def validations(context, validator):
        matches = re.findall(validator, context)
        return (len(matches) > 0) and matches[0] == context

    @staticmethod
    def validate_city_name(city_name):
        validator = "[A-Za-z0-9 ]+"
        return Validators.validations(context=city_name, validator=validator)

    @staticmethod
    def validate_latlong(lat, lon):
        try:
            lat = float(lat)
            lon = float(lon)
        except TypeError or ValueError:
            raise WrongInputError(
                message="Please provide appropriate longitude or latitude"
            )

        if not (lat and lon):
            raise WrongInputError(
                message="Please provide appropriate longitude or latitude"
            )

        if int(lat) > 90 or int(lat) < -90:
            raise WrongInputError(message="Please provide appropriate latitude")

        if int(lon) > 180 or int(lon) < -180:
            raise WrongInputError(message="Please provide appropriate longitude")

        return True

    @staticmethod
    def validate_days(days):
        try:
            days = int(days)
        except TypeError or ValueError:
            raise WrongInputError(message="Please provide appropriate value for days.")

        if int(days) > 3 or int(days) < 1:
            raise WrongInputError(message="You can see forecast for upto 3 days.")
