import os
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from app import app, db, limiter
from .models import Article
from werkzeug.utils import secure_filename
from pathlib import Path
from utils.image import allowed_image, remove_files
from utils.user import user_is_admin
from .schemas import ArticleSchema, ArticleCreateSchema, ArticleImageSchema



blog = Blueprint("Blog", __name__, url_prefix='/api/blog', description = "Blog Operation Endpoint")



@blog.route('/article')
class ArticleView(MethodView):
    # @blog.arguments(ArticleCreateSchema, location="files")
    @blog.arguments(ArticleCreateSchema, location="form")
    @blog.arguments(ArticleCreateSchema, location="files")
    @blog.response(201, ArticleSchema)
    def post(self, user_data, files):
        print('image : ', files['image'])
        print('user data : ', user_data)
        exist_article = Article.query.filter_by(title=user_data['title']).first()
        if exist_article:
            abort(400, message="this article title is posted previously !!")
        article = Article()
        article.title = user_data['title']
        article.body = user_data['body']
        article.user_id = user_data['user_id']
        article.save()
        image = files['image']
        if image and allowed_image(image.filename):
            directory = Path(os.path.join(app.config['UPLOAD_FOLDER'], f'article-{article.id}'))
            directory.mkdir(parents=True, exist_ok=True)
            location = os.path.join(directory ,secure_filename(image.filename))
        try:
            # remove_files(directory) # remove previous files as avatar
            image.save(location)
            article.image = location
            db.session.commit()
            return article
        except Exception as ex:
            abort(400, message=f"Error {ex} is happened !!")

@blog.route('article-image')
class ArticleImageView(MethodView):
    @blog.arguments(ArticleImageSchema, location="files")
    def post(self, user_data, files):
        image = files['image']
        title = user_data['title']
        print(title, image)