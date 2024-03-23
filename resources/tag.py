"""PromptlyHub Tag Routes"""
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import TagSchema, TagAndExampleSchema
from models import TagModel, PromptModel, ExampleModel

blp = Blueprint("tags", __name__, description="Operations on tags")


@blp.route("/prompt/<string:prompt_id>/tag")
class TagsInPrompt(MethodView):
    """Get Tags in a prompt"""
    @blp.response(200, TagSchema(many=True))
    def get(self, prompt_id):
        """Get prompt tags"""
        prompt = PromptModel.query.get_or_404(prompt_id)

        return prompt.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, prompt_id):
        """Add a new tag to the given prompt"""
        if TagModel.query.filter(TagModel.prompt_id == prompt_id, TagModel.name == tag_data["name"]).first():
            abort(400, message="A tag with that name already exists in that prompt.")

        tag = TagModel(**tag_data, prompt_id=prompt_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )
        return tag


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    """Tag Operations by id"""
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        """get the tag details"""
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(
        202,
        description="Delete a tag if no example is tagged with it.",
        example={"message": "Tag deleted."}
    )
    @blp.response(
        400,
        description="Returned if the tag is assignd to one or more examples. In this case, the tag is not deleted."
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.examples:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any examples, then try again."
        )


@blp.route("/example/<string:example_id>/tag/<string:tag_id>")
class LinkTagsToExample(MethodView):
    """Link Tags to Examples"""

    @blp.response(201, TagSchema)
    def post(self, example_id, tag_id):
        """Add Tag To Example"""
        example = ExampleModel.query.get_or_404(example_id)
        tag = TagModel.query.get_or_404(tag_id)

        if example.prompt.id != tag.prompt.id:
            abort(
                400, message="Make sure item and tag belong to the same store before linking.")

        example.tags.append(tag)

        try:
            db.session.add(example)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred while inserting the tag."
            )

        return tag

    @blp.response(200, TagAndExampleSchema)
    def delete(self, example_id, tag_id):
        """Delete Example from Tag"""
        example = ExampleModel.query.get_or_404(example_id)
        tag = TagModel.query.get_or_404(tag_id)

        example.tags.remove(tag)

        try:
            db.session.add(example)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred while deleting the tag."
            )

        return {"message": "Example removed from tag", "tag": tag, "example": example}
