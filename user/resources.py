import os
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from app import app, db, limiter
from .schemas import UserSchema, UserUpdateSchema, UserAvatarSchema
from .models import UserModel
from werkzeug.utils import secure_filename
from pathlib import Path
from utils.image import allowed_image, remove_files
from utils.user import user_is_admin



user = Blueprint("User", __name__, url_prefix='/api/user', description = "User Operation Endpoint")


@user.route("/<int:user_id>")
class UserInfoView(MethodView):
    @user.response(200, UserSchema)
    @limiter.limit("100/hour")
    @jwt_required()
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        if not user:
            return jsonify({'message':'ID is not valid'})
        return user

    @user.arguments(UserUpdateSchema)
    @user.response(200, UserSchema)
    @limiter.limit("100/hour")
    @jwt_required()
    def put(self, user_data, user_id):
        if not user_is_admin():
            abort(400, message = "You Are Not ADMIN !!")
        user = UserModel.query.get_or_404(user_id)
        if not user:
            abort(400, message="User is not Found !!")
        user.name = user_data['name']
        user.username = user_data['username']
        user.email = user_data['email']
        # user.role = int(user_data['role']) if user.is_superuser() else 2
        db.session.commit()
        return jsonify({'message' : 'User is updated successfully'})

    @jwt_required()
    def delete(self, user_id):
        if not user_is_admin():
            abort(400, message = "You Are Not ADMIN !!")
        user_remove = UserModel.query.get_or_404(user_id)
        if not user_remove:
            abort(400, message="User Not Found")
        db.session.delete(user_remove)
        db.session.commit()
        return jsonify({"message" : "User is Deleted Successfully"}), 200


@user.route("/users-list")
class UsersListView(MethodView):
    @user.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self):
        # if not user_is_admin():
        #     abort(400, message = "You Are Not ADMIN !!")
        users = UserModel.query.all()
        return users


@user.route('/user-add-avatar')
class UserAvatarView(MethodView):
    @user.arguments(UserAvatarSchema, location="files")
    @jwt_required()
    def post(self, files):
        if not files:
            abort(400, message="No Found any File")
        avatar = files['avatar']
        if avatar and allowed_image(avatar.filename):
            current_user = UserModel.query.filter_by(id=get_jwt_identity()).one_or_none()
            # ---------------------------------- directory --------------------------------------
            directory = Path(os.path.join(app.config['UPLOAD_IMAGE'], f'{current_user.id}'))
            directory.mkdir(parents=True, exist_ok=True)
            location = os.path.join(directory ,secure_filename(avatar.filename))
            # ------------------------------------------------------------------------------------
            try:
                remove_files(directory) # remove previous files as avatar
                avatar.save(location)
                current_user.avatar = location
                db.session.commit()
                return jsonify({'message':'user image is uploaded successfully'}), 200
            except Exception as ex:
                abort(400, message=f'error {ex} has been happened')
        else:
            abort(400, message='file is not standard')

