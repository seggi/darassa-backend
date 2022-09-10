from flask import jsonify, Blueprint
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.database.model_marsh import UserSchema

from api.database.models import User, UserProfile

from .. import db
from api.utils.responses import response_with
from api.utils import responses as resp


profile_view = Blueprint("profile_view", __name__,
                         url_prefix="/api/user")

user_schema = UserSchema()


@profile_view.post('/profile')
@jwt_required()
def user_complete_profile():
    user_id = get_jwt_identity()['id']
    try:
        request_data = request.json
        user = User.query.filter_by(id=user_id).first()
        if user:
            user_info = user_schema.dump(user)
            if user_info['is_school'] == True:
                if request_data['name'] is None or request_data["username"] is None or request_data['picture'] is None:
                    return response_with(resp.INVALID_INPUT_422)
                update_user = {
                    "name": request_data['name'],
                    "username": request_data['username'],
                }
                save_profile = {
                    "user_id": user_id,
                    "picture": request_data['picture'],
                    "country": request_data['country'],
                    "state": request_data['state'],
                    "city": request_data['city'],
                    "street": request_data['street']
                }
                User.query.filter_by(id=user_id).update(update_user)
                new_user_info = UserProfile(**save_profile)
                db.session.add(new_user_info)
                db.session.commit()
            return jsonify({
                "code": "success",
                "message": "Profile saved successfully. Now you can start your operation!"
            })
        else:
            return response_with(resp.UNAUTHORIZED_403)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)
