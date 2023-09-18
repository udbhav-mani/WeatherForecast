from flask import Flask
from flask import Flask
from flask_smorest import Api
from resources.pollution import blp as PollutionBlueprint
from resources.weather import blp as WeatherBlueprint
from resources.forecast import blp as ForecastBlueprint
from resources.history import blp as HistoryBlueprint


def create_app():
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Weather Forecast Rest API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    api = Api(app)

    api.register_blueprint(WeatherBlueprint)
    api.register_blueprint(PollutionBlueprint)
    api.register_blueprint(ForecastBlueprint)
    api.register_blueprint(HistoryBlueprint)

    return app
