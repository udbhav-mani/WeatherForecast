from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import WeatherSchema

blp = Blueprint("Pollution", "pollution", description="Operations on pollution")


# @blp.route("/pollution")
# class Pollution(MethodView):
#     @blp.response(200, (many=True))
#     def get(self):
#         return ItemModel.query.all()

#     @jwt_required()
#     @blp.arguments(ItemSchema)
#     @blp.response(201, ItemSchema)
#     def post(self, item_data):
#         item = ItemModel(**item_data)

#         try:
#             db.session.add(item)
#             db.session.commit()
#         except SQLAlchemyError:
#             abort(500, message="An error occurred while inserting the item.")

#         return item
