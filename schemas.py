"""schemas.py"""
from marshmallow import Schema, fields


class PlainExampleSchema(Schema):
    """Example Schema"""
    id = fields.Str(dump_only=True)
    details = fields.Str(required=True)


class ExampleUpdateSchema(Schema):
    """Example Update Schema"""
    details = fields.Str()


class PlainPromptSchema(Schema):
    """Prompt Schema"""
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)


class PromptUpdateSchema(Schema):
    """Update prompt schema"""
    title = fields.Str()
    description = fields.Str()

class ExampleSchema(PlainExampleSchema):
    prompt_id = fields.Int(required=True, load_only=True)
    details = fields.Nested(PlainPromptSchema(), dump_only=True)

class PromptSchema(PlainPromptSchema):
    examples = fields.List(fields.Nested(PlainExampleSchema()), dump_only=True)