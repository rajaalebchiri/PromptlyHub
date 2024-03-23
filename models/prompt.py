"""Prompt Model"""
from db import db


class PromptModel(db.Model):
    """Prompt model"""

    __tablename__ = "prompts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(300), unique=False, nullable=False)
    examples = db.relationship(
        "ExampleModel", back_populates="prompt", lazy="dynamic", cascade="all, delete")
    tags = db.relationship(
        "TagModel", back_populates="prompt", lazy="dynamic", cascade="all, delete")
