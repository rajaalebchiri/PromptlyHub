"""Example Model"""
from db import db


class ExampleModel(db.Model):
    """Example model"""

    __tablename__ = "examples"

    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.String(300), unique=False, nullable=False)
    prompt_id = db.Column(db.Integer, db.ForeignKey("prompts.id"), unique=False, nullable=False)
    prompt = db.relationship("PromptModel", back_populates="examples")
