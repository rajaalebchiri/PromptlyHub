""" Tag Model """

from db import db


class TagModel(db.Model):
    """ Tag Model """

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    prompt_id = db.Column(db.Integer, db.ForeignKey(
        "prompts.id"), nullable=False)

    prompt = db.relationship("PromptModel", back_populates="tags")

    examples = db.relationship(
        "ExampleModel", back_populates="tags", secondary="examples_tags")
