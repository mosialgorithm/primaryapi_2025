from marshmallow import Schema, fields, validate



class UserRegisterSchema(Schema):
    name = fields.Str(required=False)
    username = fields.Str(required=False)
    phone = fields.Str(required=True, validate=validate.Length(min=11, max=11))
    email = fields.Str(required=False)
    password = fields.Str(required=True, load_only=True)


class UserLoginSchema(Schema):
    phone = fields.Str(required=True, validate=validate.Length(min=11, max=11))
    password = fields.Str(required=True, load_only=True)


class UserPhoneSchema(Schema):
    phone = fields.Str(required=True, validate=validate.Length(min=11, max=11))

class ChangePassSchema(Schema):
    phone = fields.Str(required=True, validate=validate.Length(min=11, max=11))
    code = fields.Str(required=True, validate=validate.Length(min=6, max=6))
    password = fields.Str(required=True, load_only=True)