from marshmallow import Schema, fields
from flask_smorest.fields import Upload



class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=False)
    username = fields.Str(required=False)
    phone = fields.Str(required=True)
    email = fields.Str(required=False)
    password = fields.Str(required=True, load_only=True)
    role = fields.Integer(dump_only=True)
    avatar = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class UserRegisterSchema(Schema):
    name = fields.Str(required=False)
    username = fields.Str(required=False)
    phone = fields.Str(required=True)
    email = fields.Str(required=False)
    password = fields.Str(required=True, load_only=True)


class UserLoginSchema(Schema):
    phone = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    
