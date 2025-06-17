from marshmallow import Schema, fields, validate
from flask_smorest.fields import Upload




class UserSchema(Schema):
    id = fields.Int(dump_only=True) # dump_only --> serialization
    name = fields.Str(required=False)
    username = fields.Str(required=False)
    phone = fields.Str(required=True, validate=validate.Length(min=11, max=11))
    email = fields.Str(required=False)
    password = fields.Str(required=True, load_only=True) # load_only --> deserilization
    role = fields.Integer(dump_only=True)
    avatar = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class UserUpdateSchema(Schema):
    name = fields.Str(required=False)
    username = fields.Str(required=False)
    email = fields.Str(required=False)


class UserAvatarSchema(Schema):
    # avatar = Upload(required=True, format="binary")
    avatar = Upload()