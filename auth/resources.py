import random
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required
from app import db, limiter
from user.models import UserModel
from user.schemas import UserSchema, UserLoginSchema, UserRegisterSchema
from blocklist import BLOCKLIST


auth = Blueprint("Auth", __name__, url_prefix='/api/auth', description = "Authentication Endpoint")


@auth.route("/register")
class UserRegisterView(MethodView):
    @auth.arguments(UserRegisterSchema)
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
        
@auth.route('/login')
class UserloginView(MethodView):
    @auth.arguments(UserLoginSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.phone == user_data['phone']).first()
        if user:
            if user.check_password(user_data['password']):
                access_token = create_access_token(identity=str(user.id), fresh=True)
                refresh_token = create_refresh_token(str(user.id))
                return jsonify({
                    "access token" : access_token,
                    "refresh token" : refresh_token,
                }), 200
            else:
                return jsonify({
                    "message" : "password is wrong",
                    "status" : "wrong"
                })
        else:
            return jsonify({
                    "message" : "user is not found !!",
                    "status" : "wrong"
                })
        
@auth.route('/logout')
class UserLogoutView(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return jsonify({
            "message" : "User is Remove from Server",
            "status":"remove"
        }), 200
    
@auth.route('/whoami')
class UserStatusView(MethodView):
    @auth.response(200, UserSchema)
    @jwt_required()
    def get(self):
        user = UserModel.query.filter_by(id=get_jwt_identity()).one_or_none()
        return user