""" Example Tags Model """

from db import db


class ExampleTagsModel(db.Model):
    """ Example Tags Model """

    __tablename__ = "examples_tags"

    id = db.Column(db.Integer, primary_key=True)
    example_id = db.Column(db.Integer, db.ForeignKey("examples.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
