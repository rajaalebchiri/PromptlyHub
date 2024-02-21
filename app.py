"""PromptlyHub API"""
import uuid
from flask import Flask, request, jsonify
from flask_smorest import abort
from db import examples, prompts

app = Flask(__name__)

# Prompt Actions


# @app.get("/prompts")
# def get_prompts():
#     """Retriee the list of prompts"""
#     return {"prompts": list(prompts.values())}, 200


# @app.get("/prompt/<string:prompt_id>")
# def get_prompt(prompt_id):
#     """Retrieve Prompt by id"""
#     try:
#         return prompts[prompt_id], 200
#     except KeyError:
#         abort(404, "Prompt not found.")


# @app.post("/prompt")
# def create_prompt():
#     """Create a new prompt"""
#     request_data = request.get_json()
#     if ("title" not in request_data
#             or "description" not in request_data):
#         return "Prompt title and description are required.", 400

#     for prompt in prompts.values():
#         print(prompt)
#         if (
#             request_data["title"] == prompt["title"]
#         ):
#             return "Prompt already exists", 400

#     prompt_id = uuid.uuid4().hex
#     new_prompt = {**request_data, "id": prompt_id}
#     prompts[prompt_id] = new_prompt
#     return new_prompt, 201


# @app.put("/prompt/<string:prompt_id>")
# def update_prompt(prompt_id):
#     """Update Prompt by id"""
#     prompt_data = request.get_json()
#     if "title" not in prompt_data or "description" not in prompt_data:
#         return {"message": "Ensure 'title', and 'description' are included in the JSON payload"}, 400

#     try:
#         prompt = prompts[prompt_id]
#         prompt |= prompt_data

#         return prompt, 200
#     except KeyError:
#         return {"message": "prompt not found."}, 404

# @app.delete("/prompt/<string:prompt_id>")
# def delete_prompt(prompt_id):
#     """Delete Prompt by id"""
#     try:
#         del prompts[prompt_id]
#         return {"message": "Prompt deleted successfully."}
#     except KeyError:
#         return {"message": "Prompt not found."}, 404

# Example Actions



@app.post("/example")
def create_example():
    """Add example to the specified prompt"""
    request_data = request.get_json()

    if "prompt" not in request_data or "prompt_id" not in request_data:
        return "Example prompt and prompt_id are required", 400

    for example in examples.values():
        if (
            request_data["prompt"] == example["prompt"]
            and request_data["prompt_id"] == example["prompt_id"]
        ):
            return "Example already exists", 400

    if request_data["prompt_id"] not in prompts:
        abort(404, "Prompt not found.")

    example_id = uuid.uuid4().hex
    example = {**request_data, "id": example_id}
    examples[example_id] = example

    return example, 201


@app.get("/prompt/<string:prompt_id>/examples")
def get_prompt_examples(prompt_id):
    """Retreive Prompt examples by id"""
    if prompt_id not in prompts.keys():
        abort(404, "Prompt not found.")
    return [
        example
        for example in list(examples.values())
        if example["prompt_id"] == prompt_id
    ], 200


@app.put("/example/<string:example_id>")
def update_example(example_id):
    """Update Example by id"""
    example_data = request.get_json()
    if "prompt" not in example_data or "prompt_id" not in example_data:
        return {"message": "Ensure 'prompt', and 'prompt_id' are included in the JSON payload"}, 400

    try:
        example = examples[example_id]
        example |= example_data

        return example, 200
    except KeyError:
        return {"message": "example not found."}, 404


@app.delete("/example/<string:example_id>")
def delete_example(example_id):
    """ Delete example by id """
    try:
        del examples[example_id]
        return {"message": "Example deleted successfully"}
    except KeyError:
        abort(404, message="Example not found")
