"""PromptlyHub Prompt Routes"""
import uuid
from flask import Flask, request, jsonify
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import examples, prompts

blp = Blueprint("prompts", __name__, description="Operations on prompts")


@blp.route("/prompt/<string:prompt_id>")
class Prompt(MethodView):
    """Prompt class to handle prompt actions by prompt id"""
    def get(self, prompt_id):
        """Retrieve Prompt by id"""
        try:
            return prompts[prompt_id], 200
        except KeyError:
            abort(404, "Prompt not found.")

    def delete(self, prompt_id):
        """Delete Prompt by id"""
        try:
            del prompts[prompt_id]
            return {"message": "Prompt deleted successfully."}
        except KeyError:
            return {"message": "Prompt not found."}, 404

    def update(self, prompt_id):
        """Update Prompt by id"""
        prompt_data = request.get_json()
        if "title" not in prompt_data or "description" not in prompt_data:
            return {"message": "Ensure 'title', and 'description' are included in the JSON payload"}, 400

        try:
            prompt = prompts[prompt_id]
            prompt |= prompt_data

            return prompt, 200
        except KeyError:
            return {"message": "prompt not found."}, 404

@blp.route("/prompt")
class PromptList(MethodView):
    """Prompt class to handle get, post actions"""
    def get(self):
        """Retriee the list of prompts"""
        return {"prompts": list(prompts.values())}, 200
  
    def post(self):
        """Create a new prompt"""
        request_data = request.get_json()
        if ("title" not in request_data
                or "description" not in request_data):
            return "Prompt title and description are required.", 400

        for prompt in prompts.values():
            print(prompt)
            if (
                request_data["title"] == prompt["title"]
            ):
                return "Prompt already exists", 400

        prompt_id = uuid.uuid4().hex
        new_prompt = {**request_data, "id": prompt_id}
        prompts[prompt_id] = new_prompt
        return new_prompt, 201
