from datetime import datetime


class ResponseParser:
    @staticmethod
    def parse_weather_response(response):
        response = response.json()

        temp = response["main"]["temp"]
        temp_max = response["main"]["temp_max"]
        temp_min = response["main"]["temp_min"]
        feels_like = response["main"]["feels_like"]
        humidity = response["main"]["humidity"]
        pressure = response["main"]["pressure"]
        sunrise = datetime.fromtimestamp(response["sys"]["sunrise"])
        sunset = datetime.fromtimestamp(response["sys"]["sunset"])
        localtime = datetime.fromtimestamp(response["dt"])
        lat = response["coord"]["lat"]
        lon = response["coord"]["lon"]
        cityname = response["name"]

        return_dict = {
            "status": "success",
            "temp": temp,
            "max_temp": temp_max,
            "min_temp": temp_min,
            "feels_like": feels_like,
            "pressure": pressure,
            "humidity": humidity,
            "astro": {"sunrise": sunrise, "sunset": sunset},
            "location": {
                "city_name": cityname,
                "lat": lat,
                "lon": lon,
                "localtime": localtime,
            },
        }
        return return_dict

    @staticmethod
    def parse_forecast_response(response):
        response = response.json()
        lat = response["location"]["lat"]
        lon = response["location"]["lon"]
        cityname = response["location"]["name"]

        ans = []
        forecast_days = response["forecast"]["forecastday"]
        for day in forecast_days:
            temp = day["day"]["avgtemp_c"]
            temp_max = day["day"]["maxtemp_c"]
            temp_min = day["day"]["mintemp_c"]
            humidity = day["day"]["avghumidity"]
            date = datetime.fromtimestamp(day["date_epoch"])
            chance_of_rain = day["day"]["daily_will_it_rain"]
            condition = day["day"]["condition"]["text"]

            return_dict = {
                "status": "success",
                "temp": temp,
                "max_temp": temp_max,
                "min_temp": temp_min,
                "humidity": humidity,
                "location": {
                    "city_name": cityname,
                    "lat": lat,
                    "lon": lon,
                    "localtime": date,
                },
                "chance_of_rain": chance_of_rain,
                "condition": condition,
            }
            ans.append(return_dict)
        return ans
