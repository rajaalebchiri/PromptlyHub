"""PromptlyHub Example Routes"""
import uuid
from flask import Flask, request, jsonify
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import examples, prompts

blp = Blueprint("examples", __name__, description="Operations on examples")

@blp.route("/example/<string:example_id>")
class Example(MethodView):
    def get(self, example_id):
        """Retrieve Example by id"""
        try:
            return examples[example_id], 200
        except KeyError:
            abort(404, "Example not found.")
    
    def delete(self, example_id):
        pass
    
    def put(self, example_id):
        pass