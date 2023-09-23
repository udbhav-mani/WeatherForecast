import requests
import logging

logger = logging.getLogger(__name__)


class Forecast:
    FORECAST_URI = "http://127.0.0.1:5000/forecast"

    def get_forecast_by_city(self, cityname=None, days=None):
        logger.debug(f"get_forecast_by_city called with params: {cityname}, {days}")

        response = requests.get(
            self.FORECAST_URI + f"/{cityname}", params={"days": days}
        )

        if response.status_code == 500 or response.status_code == 404:
            error = response.json().get("error").get("message")
            logger.error(f"get_forecast_by_city called with error : {error}")
            return {
                "status": "failure",
                "error": {"code": 500, "message": error},
            }
        else:
            return response.json()

    def get_forecast_by_latlon(self, lat=None, lon=None, days=None):
        logger.debug(f"get_forecast_by_latlon called with params: {lat}, {lon}, {days}")

        response = requests.get(
            self.FORECAST_URI,
            params={"lat": f"{lat}", "lon": f"{lon}", "days": days},
        )

        if response.status_code == 500 or response.status_code == 404:
            error = response.json().get("error").get("message")
            logger.error(f"get_forecast_by_latlon called with error : {error}")
            return {
                "status": "failure",
                "error": {"code": 500, "message": error},
            }
        else:
            return response.json()
