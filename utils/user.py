from flask import abort
from user.models import UserModel
from flask_jwt_extended import get_current_user, get_jwt_identity




# ----------- just superuser can edit any user ---------------
def user_is_admin():
    current_user = UserModel.query.filter_by(id=get_jwt_identity()).one_or_none()
    if not current_user.is_admin():
        # return abort(400, message = "You Are Not ADMIN !!")
        return False
    return True
