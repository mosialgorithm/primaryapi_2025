from marshmallow import Schema, fields
from flask_smorest.fields import Upload



class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=False)
    username = fields.Str(required=False)
    phone = fields.Str(required=True)
    email = fields.Str(required=False)
    password = fields.Str(required=True, load_only=True)

    
