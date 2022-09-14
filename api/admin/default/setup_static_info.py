from this import s
from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.database.model_marsh import StudentAddressSchema, StudentParentSchema, StudentsSchema, UserSchema
from api.database.models import Classes, StudentAddress, StudentParent, Students, User

from ... import db
from api.utils.responses import Response, response_with
from api.utils import responses as resp

setup_static_info = Blueprint("setup_static_info", __name__,
                              url_prefix="/api/user/admin")


@setup_static_info.post('/setup-classes')
@jwt_required(refresh=True)
def setup_classes():
    school_id = get_jwt_identity()['id']
    try:
        request_data = request.json

        school_class = db.session.query(Classes).filter(
            Classes.school_id == school_id).first()

        if request_data['name'] is None:
            return response_with(resp.INVALID_INPUT_422)

        if school_class:
            return Response.success(message="Class name already added.")

        new_data = {
            "school_id": school_id,
            "name": request_data["name"]
        }

        school_classes = Classes(**new_data)
        db.session.add(school_classes)
        db.session.commit()

        return Response.created(message="Class added with success.")

    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)
