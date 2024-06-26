"""PromptlyHub Prompt Routes"""
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_sqlalchemy import SQLAlchemy, pagination

from db import db
from schemas import PromptSchema, PromptUpdateSchema
from models import PromptModel, TagModel


blp = Blueprint("prompts", __name__, description="Operations on prompts")


@blp.route("/prompt/<int:prompt_id>")
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
        db.session.delete(prompt)
        db.session.commit()
        return {"message": "Prompt deleted successfully"}, 200

    @blp.arguments(PromptUpdateSchema)
    @blp.response(200, PromptSchema)
    def put(self, prompt_data, prompt_id):
        """Update Prompt by id"""

        prompt = PromptModel.query.get(prompt_id)

        if prompt:
            prompt.title = prompt_data["title"]
            prompt.description = prompt_data["description"]

        else:
            prompt = PromptModel(id=prompt_id, **prompt_data)

        db.session.add(prompt)
        db.session.commit()

        return prompt


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
        """Retrieve the list of prompts"""
        page = request.args.get("page", type=int)
        per_page = request.args.get("per_page", type=int)
        
        if page and per_page:

            pagination_query = PromptModel.query.paginate(
                page=page, per_page=per_page, error_out=False)

            prompts = pagination_query.items

            return prompts
        return PromptModel.query.all()

@blp.route("/prompts/<tag>")
class PromptsByCategory(MethodView):
    """Get a list of prompts by category"""

    @blp.response(200, PromptSchema(many=True))
    def get(self, tag):
        """Retrieve the list of prompts by category"""
        print(tag)
        category = TagModel.query.filter(TagModel.name == tag).first()
        print(category)
        if category:
            prompts = PromptModel.query.filter(
                PromptModel.tags.any(name=tag)).all()
            if prompts:
                return PromptSchema(many=True).dump(prompts)
            return "No prompts found for this category", 404
        return "Category not found", 404
