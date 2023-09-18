from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import LocationSchema
from schemas import WeatherSchema

blp = Blueprint("Weather", "Weather", description="Operations on weather")


@blp.route("/weather")
class Weather(MethodView):
    @blp.response(200, WeatherSchema)
    def get(self):
        pass

    @blp.arguments(LocationSchema)
    @blp.response(201, WeatherSchema)
    def post(self, item_data):
        pass
