from marshmallow import Schema, fields, validate
from flask_smorest.fields import Upload
# from werkzeug.datastructures import FileStorage


class ArticleSchema(Schema):
    id = fields.Int(dump_only=True)
    article_id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    # body = fields.Text(required=True)
    body = fields.Str(required=True)
    # image = fields.Str(required=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ArticleCreateSchema(Schema):
    title = fields.String()
    body = fields.String()
    user_id = fields.Int()
    image = Upload()
    # user_id = fields.Int(load_default=1)
    # file = fields.Raw()
    # body = fields.Text(required=True)
    # image = fields.Raw(type='file', format='binary', required=True, description='The uploaded file')
    # image = fields.Raw()
    # user_id = fields.Int(required=True)

class ArticleImageSchema(Schema):
    title = fields.Str(required=True)
    image = Upload()