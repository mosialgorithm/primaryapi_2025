import random
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required
from app import db, limiter
from user.models import UserModel
from user.schemas import UserSchema
from blocklist import BLOCKLIST


auth = Blueprint("Auth", __name__, url_prefix='/api/auth', description = "Authentication Endpoint")


@auth.route("/register")
class UserRegisterView(MethodView):
    @auth.arguments(UserSchema)
    @auth.response(201, UserSchema)
    @limiter.limit("100/hour")
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.phone == user_data["phone"]).first()
        if user:
            abort(409, message="Phone Number is Registered by Another User")
        # 
        user = UserModel()
        user.name = user_data["name"]
        user.username = user_data["username"]
        user.phone = user_data["phone"]
        user.email = user_data["email"]
        user.set_password(user_data["password"])
        try:
            db.session.add(user)
            db.session.commit()
            return user
            # return jsonify({
            #     "message" : "User is Created Successfully",
            #     "data" : user
            # }), 201
        except Exception as ex:
            db.session.rollback()
            return jsonify({"message": f"Error {ex} is Happened"}), 400