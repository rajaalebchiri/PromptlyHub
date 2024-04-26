"""schemas.py"""
from marshmallow import Schema, fields


class PlainExampleSchema(Schema):
    """Example Schema"""
    id = fields.Str(dump_only=True)
    details = fields.Str(required=True)
    description = fields.Str(required=False)


class PlainPromptSchema(Schema):
    """Prompt Schema"""
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class PromptSchema(PlainPromptSchema):
    """Prompt schema"""
    examples = fields.List(fields.Nested(PlainExampleSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))


class ExampleSchema(PlainExampleSchema):
    """Example Schema"""
    prompt_id = fields.Int(required=True, load_only=True)
    prompt = fields.Nested(PlainPromptSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))


class TagSchema(PlainTagSchema):
    """Tag Schema"""
    prompt_id = fields.Int(load_only=True)
    prompt = fields.Nested(PlainPromptSchema(), dump_only=True)
    examples = fields.List(fields.Nested(PlainExampleSchema(), dump_only=True))


class ExampleUpdateSchema(Schema):
    """Example Update Schema"""
    details = fields.Str()
    description = fields.Str()


class PromptUpdateSchema(Schema):
    """Update prompt schema"""
    title = fields.Str()
    description = fields.Str()


class TagAndExampleSchema(Schema):
    """Tag and example schema"""
    message = fields.Str()
    example = fields.Nested(ExampleSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)
