from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_migrate import Migrate
from config import Developement
from blocklist import BLOCKLIST
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS




app = Flask(__name__)
app.config.from_object(Developement)
# CORS(app)
# CORS(app, resources={r'/*': origins: '*'})
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# .............................................................................................
api = Api(app)
jwt = JWTManager(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
            }
        ),
        401,
    )

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )



# ............................................. API_Blueprint .............................................
from auth.resources import auth
from user.resources import user
from blog.resources import blog



api.register_blueprint(auth)
api.register_blueprint(user)
api.register_blueprint(blog)
# ............................................. End_Of_API_Blueprint .......................................



# @app.route('/')
# def index():
#     return jsonify({
#         "app name" : "Flask Rest API Primary",
#         "developer" : "mosiweb.ir",
#         "year" : "1404"
#         })



if __name__ == '__main__':
    app.run()