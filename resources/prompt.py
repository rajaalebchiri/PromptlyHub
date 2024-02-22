"""PromptlyHub Prompt Routes"""
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import PromptSchema, PromptUpdateSchema
from models import PromptModel


blp = Blueprint("prompts", __name__, description="Operations on prompts")


@blp.route("/prompt/<string:prompt_id>")
class Prompt(MethodView):
    """Prompt class to handle prompt actions by prompt id"""

    @blp.response(200, PromptSchema)
    def get(self, prompt_id):
        """Retrieve Prompt by id"""
        prompt = PromptModel.query.get_or_404(prompt_id)
        return prompt

    def delete(self, prompt_id):
        """Delete Prompt by id"""
        prompt = PromptModel.query.get_or_404(prompt_id)
        raise NotImplementedError("Deleting an example is not implemented.")

    @blp.arguments(PromptUpdateSchema)
    @blp.response(200, PromptSchema)
    def put(self, prompt_data, prompt_id):
        """Update Prompt by id"""

        prompt = PromptModel.query.get_or_404(prompt_id)
        raise NotImplementedError("Deleting an example is not implemented.")


@blp.route("/prompt")
class PromptPost(MethodView):
    """Prompt class to handle post action"""

    @blp.arguments(PromptSchema)
    @blp.response(201, PromptSchema)
    def post(self, request_data):
        """Create a new prompt"""

        prompt = PromptModel(**request_data)
        try:
            db.session.add(prompt)
            db.session.commit()

        except IntegrityError:
            abort(500,
                  message="A prompt with that title already exists.")

        except SQLAlchemyError:
            abort(500,
                  message="An error occurred creating the prompt.")
        
        return prompt


@blp.route("/prompts")
class PromptList(MethodView):
    """Prompt class to handle get actions"""

    @blp.response(200, PromptSchema(many=True))
    def get(self):
        """Retriee the list of prompts"""
        prompt = PromptModel.query
        print(prompt)
        raise NotImplementedError("Deleting an example is not implemented.")
