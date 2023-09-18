from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PollutionSchema, LocationSchema

blp = Blueprint("Pollution", "pollution", description="Operations on pollution")


@blp.route("/pollution")
class Pollution(MethodView):
    @blp.response(200, PollutionSchema(many=True))
    def get(self):
        pass

    @blp.arguments(LocationSchema)
    @blp.response(201, PollutionSchema)
    def post(self, item_data):
        pass
