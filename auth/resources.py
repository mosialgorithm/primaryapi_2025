import random
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required
from app import db, limiter
from user.models import UserModel
from .schemas import UserLoginSchema, UserRegisterSchema, UserPhoneSchema, ChangePassSchema
from user.schemas import UserSchema
from blocklist import BLOCKLIST
from datetime import datetime, timedelta




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
    def get(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return jsonify({
            "message" : "User is loged out from Server",
            "status":"logout"
        }), 200
    

@auth.route('/whoami')
class UserStatusView(MethodView):
    @auth.response(200, UserSchema)
    @jwt_required()
    def get(self):
        user = UserModel.query.filter_by(id=get_jwt_identity()).one_or_none()
        return user


@auth.route('/reset-pass')
class ResetPassView(MethodView):
    @auth.arguments(UserPhoneSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.phone==user_data['phone']).first()
        if not user:
            return abort(404, message='this phone number is not registered yet')
        code = random.randint(0,999999)
        print('code : ', code) #TODO replace by sms
        user.code = code
        user.code_expire = datetime.now() + timedelta(minutes=1)
        db.session.commit()
        return jsonify({
            "message" : "verify code is sent to mobile number"
        })


@auth.route('/change-pass')
class ChangePassView(MethodView):
    @auth.arguments(ChangePassSchema)
    def post(self, user_data):
        user_phone = user_data['phone']
        user_code = user_data['code']
        user_password = user_data['password']
        user = UserModel.query.filter(UserModel.phone==user_phone).first()
        if not user:
            return jsonify({"message" : "phone number is incorrect"}), 404

        if datetime.now() > user.code_expire:
            user.code = None
            user.expire_code = None
            db.session.commit()
            return jsonify({"message" : "code is expired, please try again"}), 404
        if user_code == user.code:
            user.set_password(user_password)
            user.code = None
            db.session.commit()
            return jsonify({'message' : 'password is changed successfully'}), 200
        else:
            return jsonify({"message" : "code is wrong"}), 404


