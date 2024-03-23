"""PromptlyHub Example Routes"""

from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db
from schemas import ExampleSchema, ExampleUpdateSchema
from models import ExampleModel

blp = Blueprint("examples", __name__, description="Operations on examples")


@blp.route("/example/<string:example_id>")
class Example(MethodView):
    """Handle Requests with Example id"""

    @blp.response(200, ExampleSchema)
    def get(self, example_id):
        """Retrieve Example by id"""

        example = ExampleModel.query.get_or_404(example_id)
        return example

    def delete(self, example_id):
        """ Delete example by id """
        example = ExampleModel.query.get_or_404(example_id)
        raise NotImplementedError("Deleting an example is not implemented.")

    @blp.arguments(ExampleUpdateSchema)
    @blp.response(200, ExampleSchema)
    def put(self, example_data, example_id):
        """Update Example by id"""
        example = ExampleModel.query.get(example_id)

        if example:
            example.details = example_data["details"]

        else:
            example = ExampleModel(id=example_id, **example_data)

        db.session.add(example)
        db.session.commit()

        return example

@blp.route("/example")
class ExamplePost(MethodView):
    """Handle Example Post request"""

    @blp.response(200, ExampleSchema(many=True))
    def get(self):
        """Get Example list"""
        example = ExampleModel.query.get()
        raise NotImplementedError("Deleting an example is not implemented.")

    @blp.arguments(ExampleSchema)
    @blp.response(201, ExampleSchema)
    def post(self, request_data):
        """Add example to the specified prompt"""
        example = ExampleModel(**request_data)

        try:
            db.session.add(example)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return example
